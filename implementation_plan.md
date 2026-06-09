# Implementation Plan - Simplified Customizer Form (Photo, Text, Both)

We will roll back the interactive canvas visual editor and replace it with a clean, simplified product customization form. This restores the exact customization experience used prior to the visual editor work, while maintaining support for fabric colors (Purple, White, Black) and sizes (S, M, L, XL, XXL, XXXL) for apparel.

## User Review Required

> [!IMPORTANT]
> - **Simplified 2-Column Customizer Layout:** The overlay is simplified to a static front-view mockup preview of the product (left column) and the customization form inputs (right column).
> - **Customization Options (Photo, Text, Both):** The user can choose between three tab modes:
>   1. **Photo**: Upload a photograph dropzone.
>   2. **Text**: Custom text input field.
>   3. **Both**: Show both the upload dropzone and the custom text input field.
> - **No Interactive Editing:** Drag-and-drop event listeners, double-clicks to center, scale sliders, views sidebar, and sliding drawers are completely removed.
> - **Apparel Properties (Color & Size):** Fabric color choices (Purple, White, Black) and sizes (S to XXXL) remain as visible option rows on the form for apparel products (T-Shirt, Polo Shirt, Gifting Box).
> - **Database Compatibility:** Customization type "Both" is mapped internally to type "photo" and bundles the photograph base64 in `customization_data` with the text appended to `customization_summary` to prevent schema violations.

---

## Proposed Changes

### Frontend Components

#### [MODIFY] [index.html](file:///c:/Users/anaka/Downloads/third%20app/third%20app/index.html)
- Clean up `#customizer-modal-overlay` structure:
  - Remove views sidebar `.customizer-views-sidebar`.
  - Remove grid actions `.customizer-actions-grid`.
  - Remove sliding drawers `.customizer-drawers-container`.
  - Add tab selection row for **Photo**, **Text**, and **Both** types.
  - Add simple form input groups for File Upload and Custom Text.
  - Place Fabric Color swatch selection and Size selector swatches directly on the right panel as static form elements.
  - Simplify description and price rows at the bottom.

#### [MODIFY] [app.js](file:///c:/Users/anaka/Downloads/third%20app/third%20app/app.js)
- Remove mouse and touch dragging listeners (`mousedown`, `mousemove`, `mouseup`, etc.) from `productCatalog.init()`.
- Remove coordinate state variables (`photoX`, `photoY`, `photoScale`, `textX`, `textY`) or set them as static values.
- Rewrite `openCustomizer(productId)`:
  - Reset form inputs (text input, file input, color active swatch, size active swatch).
  - Reset static canvas preview layers (photo and text).
  - Set default active tab to `'photo'`.
  - Toggle visibility of color and size selectors (visible only if T-Shirt, Polo Shirt, or Gifting Box).
  - Render front-view SVG mockup and set fabric color.
- Implement `switchTab(tabName)`:
  - Update active tab styling.
  - Toggle visibility of the upload dropzone and text inputs based on the selected tab (Photo: show upload; Text: show text; Both: show both).
  - Update static canvas previews accordingly.
- Update `updateTextContent(val)` to update the `#canvas-custom-text` element and center it statically in the print zone.
- Update `applyCustomization()`:
  - Validate that a fabric color and size are selected if the product is apparel.
  - Validate that the photo is uploaded (for Photo/Both) or that the text is filled (for Text/Both).
  - Construct cart item customization payload:
    - If "Both" is selected, set type to `'photo'`, data to the photo base64, and summary to `Customized Blueprint (Photo & Text: "${textVal}")${colorSuffix}`.
    - If "Photo", set type to `'photo'`, data to the photo base64, and summary to `Customized Blueprint (Photograph)${colorSuffix}`.
    - If "Text", set type to `'text'`, data to the text string, and summary to `Customized Blueprint (Text: "${textVal}")${colorSuffix}`.

---

## Verification Plan

### Automated Tests
- Run `.\backend\.venv\Scripts\python backend/manage.py test api` to make sure all 10 Django unit tests remain green.

### Manual Verification
- Open customizer: check that it loads the realistic front-mockup on the left and form controls on the right.
- Switch tabs: verify "Photo" displays the upload dropzone, "Text" displays the input field, and "Both" displays both inputs.
- Validate validation rules: check that "Save & Proceed" fires alerts if color/size is missing for apparel, or if photo/text inputs are blank.
- Complete customization: add customized product to cart and verify order summary displays correct colors, sizes, and customization summary format.
