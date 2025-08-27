# Changelog

All notable changes to this project will be documented in this file.

---

## [1.1.0] - 2025-08-27

### Added
- **Cloudinary Integration:** The project now uses Cloudinary for robust, cloud-based handling of all image assets, including product and category images.
- **Dynamic Copyright Year:** The copyright year in the footer is now generated dynamically using a Flask template context processor, ensuring it's always up-to-date.
- **Styling Hook for Add Product Form:** An ID has been added to the `AddProductForm` to make it easier for the frontend team to apply specific styles.
- **Project Documentation:** Added comprehensive documentation to the codebase to clarify new features and architecture.

### Changed
- **Image Upload Workflow:** The entire image upload logic has been transitioned from local storage to the Cloudinary service.
- **Product Model:** The `images` field in the `Products` model is now a non-nullable JSON type to natively store a list of image URLs.
- **Dependencies & Configuration:** Updated `requirements.txt` with new packages and modified the `.env` file to include necessary keys for the Cloudinary API.
- **Code Refactoring:** Cleaned up various routes and services for improved readability and maintainability.
- **UX Enhancements:** Implemented various styling and user experience improvements across the application.

### Fixed
- **Critical Image Upload Bug:** Resolved a major issue where a product could be created with an empty list of images if all file uploads failed. The system now requires at least one successful upload to proceed.

### Security
- **Hardened Logout Route:** The user logout endpoint now only accepts POST requests, mitigating Cross-Site Request Forgery (CSRF) vulnerabilities.

### Notes for Frontend Team
- The `AddProductForm` on the `/product/add-product` page is ready for styling. A container div with the class `add-product-form-container` has been added, and specific styling for the `MultipleFileField` is required. Please refer to the updated template for the new structure.