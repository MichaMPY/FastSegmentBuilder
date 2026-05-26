<img width="1557" height="972" alt="fastsegbild" src="https://github.com/user-attachments/assets/f6197f22-481a-4ffd-8ae5-e26af2741079" />
# Fast Segment Builder

**Fast persistent threshold-based segmentation workflow for 3D Slicer with protected multi-segment editing.**

## Overview
Fast Segment Builder is a custom module for 3D Slicer designed to accelerate multi-segment thresholding. It allows independent thresholding for each segment without damaging previously created structures.

## Key Features
* **Persistent UI:** Custom buttons stay saved between Slicer sessions using QSettings.
* **Data Integrity:** Automatically sets `OverwriteNone` mode to protect existing segments from accidental corruption.
* **Auto-Logical Ops:** Automatically detects overlaps and performs subtractions.
* **Research Optimized:** Built specifically for large trauma and multi-organ CT/MRI datasets.

## Technical Implementation
The module ensures stable multi-segment editing by forcing the segment editor's overwrite mode:
```python
editNode.SetOverwriteMode(slicer.vtkMRMLSegmentEditorNode.OverwriteNone)
## Installation

To use this module in 3D Slicer, follow these steps:

1. **Download the code:** Click the green **Code** button and select **Download ZIP**. Unzip the archive to a folder on your computer.
2. **Open 3D Slicer:**
   Go to the top menu: **Edit** -> **Application Settings**.
3. **Add the Module Path:**
   - Select **Modules** in the left sidebar.
   - Click the **Add** button (or the "..." next to "Additional module paths").
   - Select the folder where you unzipped the repository (the folder containing `FastSegmentBuilder.py`).
4. **Restart Slicer:**
   Slicer will ask to restart. Click **Yes**.
5. **Find the Module:**
   Once restarted, you can find the tool in the module selector under the **Segmentation** category.
