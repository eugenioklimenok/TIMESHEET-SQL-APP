# 🔄 Cómo actualizar tu entorno local desde GitHub

Cuando hacés cambios directamente desde la web de GitHub (por ejemplo, subir o editar archivos `.md`, `.sql`, etc.), tu entorno local **no se actualiza automáticamente**.

Este mini tutorial te guía paso a paso para sincronizar tu entorno local (por ejemplo, en tu VM Linux) con el repositorio remoto.

---

## ✅ PASO 1: Abrí tu terminal en la carpeta del proyecto

```bash
cd ~/ruta/a/tu/proyecto
```

---

## ✅ PASO 2: Verificá en qué rama estás

```bash
git branch
```

> Deberías estar en `main` (o `master`). Si no, cambiá con:

```bash
git checkout main
```

---

## ✅ PASO 3: Ejecutá `git pull` para traer los cambios

```bash
git pull origin main
```

Esto va a sincronizar tu entorno local con los cambios hechos desde GitHub.

---

## 🧪 Extra: Verificar últimos cambios

### Últimos 5 commits

```bash
git log --oneline -n 5
```

### Ver archivos modificados localmente

```bash
git status
```

