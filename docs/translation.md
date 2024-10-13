
# Translation Guide

This document outlines the procedure for incorporating a new language into the project.

## Workflow Overview

1. **Register the New Language**
   Add the desired language to the `LANGUAGES` list within the [`settings/locale.py`](../routine_tracker/project/settings/locale.py) file.

2. **Generate Translation Files**
   Execute the following command to initialize the necessary translation files:

   ```bash
   make translations
   ```

3. **Provide Translations**
   Open the `.po` files located in the `locale` directory and translate the required text strings.

4. **Compile Translations**
   Convert the `.po` files into `.mo` files by running:

   ```bash
   make compile-translations
   ```

5. **Apply Changes to the Database**
   Ensure the new language is registered by updating the database with the command:

   ```bash
   make migrate
   ```

## Additional Considerations

- This procedure can also be used to modify translations for existing languages.
- All translation files are located in the [`locale`](../routine_tracker/project/locale/) directory.

## Further Reading

- [Django Translation Documentation](https://docs.djangoproject.com/en/5.1/topics/i18n/translation/)
- [Guide to Internationalization in Django](https://reintech.io/blog/django-internationalization-tutorial)
