# 🔒 Configuración de Credenciales

Esta carpeta contiene archivos de configuración para el sistema de automatización FDA/Shopify.

## 📋 Configuración Inicial

### Para nuevos usuarios:

1. **Copiar archivos template:**
   ```bash
   cp config/secrets.py.template config/secrets.py
   cp config/config.py.template config/config.py
   ```

2. **Editar `config/secrets.py` con tus credenciales:**
   ```python
   # Configuración de Shopify
   SHOPIFY_CONFIG = {
       "SHOP": "tu-tienda",  # sin .myshopify.com
       "TOKEN": "shpat_tu_token_aqui",
       "API_VERSION": "2023-07"
   }

   # Configuración de FDA
   FDA_CONFIG = {
       "USERNAME": "tu_usuario_fda",
       "PASSWORD": "tu_password_fda"
   }
   ```

3. **¡Listo!** El archivo `config.py` se configurará automáticamente.

## 🔐 Seguridad

- ✅ `secrets.py` y `config.py` están en `.gitignore`
- ✅ Nunca se subirán al repositorio
- ✅ Solo los archivos `.template` se comparten públicamente

## 📁 Archivos

| Archivo | Propósito | Se sube a Git |
|---------|-----------|---------------|
| `secrets.py.template` | Plantilla para credenciales | ✅ Sí |
| `config.py.template` | Plantilla para configuración | ✅ Sí |
| `secrets.py` | Tus credenciales reales | ❌ No (local) |
| `config.py` | Tu configuración real | ❌ No (local) |

## 🚨 Importante

**NUNCA** edites los archivos `.template` con credenciales reales. Solo edita los archivos sin `.template`. 