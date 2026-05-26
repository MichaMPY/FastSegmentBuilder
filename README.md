<img width="1557" height="972" alt="fastsegbild" src="https://github.com/user-attachments/assets/f6197f22-481a-4ffd-8ae5-e26af2741079" />
# Fast Segment Builder

<p align="center">
  <img src="https://github.com/user-attachments/assets/f6197f22-481a-4ffd-8ae5-e26af2741079" width="1000"/>
</p>

---

# Fast Segment Builder

**Fast persistent threshold-based segmentation workflow for 3D Slicer with protected multi-segment editing.**

---

## Overview

Fast Segment Builder is a custom module for 3D Slicer designed to accelerate multi-segment threshold-based segmentation workflows.

The module allows independent thresholding for each segment without damaging previously created structures, making it especially useful for large medical imaging datasets and research pipelines.

---

## Why This Module Exists

Standard threshold workflows in 3D Slicer can accidentally overwrite previously created segments during multi-segment editing.

Fast Segment Builder solves this problem by enforcing protected overwrite behavior and automating repetitive segmentation operations.

---

## Key Features

### Persistent UI
Custom segmentation buttons are automatically saved between Slicer sessions using `QSettings`.

### Protected Multi-Segment Editing
Automatically enables `OverwriteNone` mode to prevent accidental corruption of existing segments during threshold operations.

### Automatic Logical Operations
Automatically detects overlaps between segments and performs logical subtraction operations.

### Research-Oriented Workflow
Optimized for:

- Trauma CT datasets
- Multi-organ segmentation
- Large annotation workflows
- Medical imaging research
- AI dataset preparation

---

## Technical Implementation

The module ensures stable multi-segment editing by enforcing protected overwrite behavior:

```python
editNode.SetOverwriteMode(
    slicer.vtkMRMLSegmentEditorNode.OverwriteNone
)
```

This prevents newly created threshold segments from overwriting existing structures.

---

## Built With

- Python
- Qt
- CTK
- VTK
- MRML API
- 3D Slicer Segment Editor API

---

## Installation

### Load as Local Module in 3D Slicer

1. Open 3D Slicer

2. Go to:

```text
Edit → Application Settings → Modules
```

3. Click **Add**

4. Select the folder containing:

```text
FastSegmentBuilder.py
```

5. Restart 3D Slicer

6. Open the module from:

```text
Segmentation → Fast Segment Builder
```

---

## Usage

1. Select an input volume.
2. Set lower and upper threshold values.
3. Create a custom segmentation button.
4. Click the button to generate a segment.
5. Existing segments remain protected during editing.

---

## Repository Structure

```text
FastSegmentBuilder/
│
├── FastSegmentBuilder.py
├── README.md
├── LICENSE
├── .gitignore
├── screenshots/
└── examples/
```

---

## Recommended GitHub Topics

```text
3d-slicer
medical-imaging
segmentation
vtk
python
dicom
medical-ai
radiology
annotation-tool
```

---

## License

MIT License
