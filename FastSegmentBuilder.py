import vtk
import qt
import ctk
import slicer
from slicer.ScriptedLoadableModule import *

# 1. ОСНОВНИЙ КЛАС МОДУЛЯ
class FastSegmentBuilder(ScriptedLoadableModule):
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "Fast Segment Builder"
        self.parent.categories = ["Segmentation"]
        self.parent.contributors = ["User"]
        self.parent.helpText = "Швидка сегментація на основі порогів з автоматичним відніманням для збереження анатомічної цілісності."

# 2. КЛАС ГРАФІЧНОГО ІНТЕРФЕЙСУ (WIDGET)
class FastSegmentBuilderWidget(ScriptedLoadableModuleWidget):
    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)
        self.logic = FastSegmentBuilderLogic()
        self.segmentButtons = []

        # Палітра кольорів для сегментів
        self.segmentColors = [
            (1.0, 0.0, 0.0), (1.0, 0.5, 0.0), (1.0, 1.0, 0.0), (0.5, 1.0, 0.0),
            (0.0, 1.0, 0.0), (0.0, 1.0, 1.0), (0.0, 0.5, 1.0), (0.0, 0.0, 1.0),
            (0.5, 0.0, 1.0), (1.0, 0.0, 1.0), (1.0, 0.0, 0.5)
        ]

        # --- СЕКЦІЯ ВИБОРУ ДАНИХ ---
        self.layout.addWidget(qt.QLabel("Input Volume:"))
        self.volumeSelector = slicer.qMRMLNodeComboBox()
        self.volumeSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
        self.volumeSelector.setMRMLScene(slicer.mrmlScene)
        self.volumeSelector.selectNodeUponCreation = True
        self.layout.addWidget(self.volumeSelector)

        # --- СЕКЦІЯ НАЛАШТУВАННЯ ПОРОГІВ (THRESHOLD) ---
        self.layout.addWidget(qt.QLabel("Threshold Range (Lower / Upper):"))
        self.thresholdSlider = ctk.ctkSliderWidget()
        self.thresholdSlider.minimum, self.thresholdSlider.maximum = -1000, 5000
        self.thresholdSlider.value = 200
        self.layout.addWidget(self.thresholdSlider)

        self.upperThresholdSlider = ctk.ctkSliderWidget()
        self.upperThresholdSlider.minimum, self.upperThresholdSlider.maximum = -1000, 5000
        self.upperThresholdSlider.value = 5000
        self.layout.addWidget(self.upperThresholdSlider)

        # --- СЕКЦІЯ КЕРУВАННЯ КНОПКАМИ ---
        self.layout.addWidget(qt.QLabel("Create Action Button:"))
        self.segmentNameEdit = qt.QLineEdit()
        self.segmentNameEdit.placeholderText = "e.g. Bone, Muscle, Hematoma"
        self.layout.addWidget(self.segmentNameEdit)

        self.addButton = qt.QPushButton("Add Action Button")
        self.addButton.clicked.connect(self.onAddButton)
        self.layout.addWidget(self.addButton)

        self.resetButton = qt.QPushButton("Clear Saved Buttons")
        self.resetButton.clicked.connect(self.onResetButtons)
        self.layout.addWidget(self.resetButton)

        # --- ОБЛАСТЬ ШВИДКИХ КНОПОК ---
        self.layout.addWidget(qt.QLabel("Quick Access Segmentation:"))
        self.buttonContainer = qt.QWidget()
        self.buttonLayout = qt.QVBoxLayout(self.buttonContainer)
        self.layout.addWidget(self.buttonContainer)

        # Завантаження збережених кнопок при старті
        self.loadButtons()
        self.layout.addStretch(1)

    def onAddButton(self):
        name = self.segmentNameEdit.text.strip()
        if name:
            self.createSegmentButton(name)
            self.saveButtons()
            self.segmentNameEdit.clear()

    def createSegmentButton(self, name):
        btn = qt.QPushButton(name)
        btn.clicked.connect(lambda: self.onSegmentClick(name))
        # Можливість перейменування через праву кнопку миші
        btn.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        btn.customContextMenuRequested.connect(lambda: self.onRename(btn))
        self.buttonLayout.addWidget(btn)
        self.segmentButtons.append(btn)

    def onSegmentClick(self, name):
        volume = self.volumeSelector.currentNode()
        if volume:
            self.logic.runSegmentation(volume, name, self.thresholdSlider.value, self.upperThresholdSlider.value, self.segmentColors)
            slicer.util.showStatusMessage(f"Created: {name}", 2000)

    def onRename(self, btn):
        new_name, ok = qt.QInputDialog.getText(slicer.util.mainWindow(), "Rename", "New Name:", text=btn.text)
        if ok and new_name:
            btn.setText(new_name)
            self.saveButtons()

    def onResetButtons(self):
        qt.QSettings().remove("FastSegmentBuilder/ButtonNames")
        for btn in self.segmentButtons: btn.deleteLater()
        self.segmentButtons = []

    def saveButtons(self):
        qt.QSettings().setValue("FastSegmentBuilder/ButtonNames", [b.text for b in self.segmentButtons])

    def loadButtons(self):
        names = qt.QSettings().value("FastSegmentBuilder/ButtonNames", [])
        if isinstance(names, str): names = [names]
        for name in names: self.createSegmentButton(name)

# 3. КЛАС ЛОГІКИ (ОБЧИСЛЕННЯ)
class FastSegmentBuilderLogic(ScriptedLoadableModuleLogic):
    def getSegmentationNode(self):
        node = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLSegmentationNode")
        if not node:
            node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
            node.CreateDefaultDisplayNodes()
        return node

    def runSegmentation(self, volumeNode, name, lower, upper, colors):
        segNode = self.getSegmentationNode()
        segmentation = segNode.GetSegmentation()
        
        # 1. Створення сегмента та встановлення кольору
        segID = segmentation.AddEmptySegment(name)
        segment = segmentation.GetSegment(segID)
        color = colors[(segmentation.GetNumberOfSegments() - 1) % len(colors)]
        segment.SetColor(*color)

        # 2. Налаштування невидимого редактора (Editor Node)
        editNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
        editor = slicer.qMRMLSegmentEditorWidget()
        editor.setMRMLScene(slicer.mrmlScene)
        editor.setMRMLSegmentEditorNode(editNode)
        editor.setSegmentationNode(segNode)
        editor.setSourceVolumeNode(volumeNode)
        
        # 3. Захист: забороняємо затирати існуючі сегменти (OverwriteNone)
        editNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
        editNode.SetSelectedSegmentID(segID)

        # 4. Запуск ефекту порогу (Threshold)
        editor.setActiveEffectByName("Threshold")
        effect = editor.activeEffect()
        effect.setParameter("MinimumThreshold", str(lower))
        effect.setParameter("MaximumThreshold", str(upper))
        effect.self().onApply()

        # 5. Автоматичне віднімання всіх існуючих сегментів
        editor.setActiveEffectByName("Logical operators")
        logicEffect = editor.activeEffect()
        ids = vtk.vtkStringArray()
        segmentation.GetSegmentIDs(ids)
        
        for i in range(ids.GetNumberOfValues()):
            otherID = ids.GetValue(i)
            if otherID != segID:
                editNode.SetSelectedSegmentID(segID)
                logicEffect.setParameter("Operation", "SUBTRACT")
                logicEffect.setParameter("ModifierSegmentID", otherID)
                logicEffect.setParameter("BypassMasking", "1")
                logicEffect.self().onApply()

        # 6. ФІКСАЦІЯ НАЗВИ (щоб уникнути "Segment_1")
        segment.SetName(name)

        # 7. Очищення сцени від тимчасових вузлів
        slicer.mrmlScene.RemoveNode(editNode)