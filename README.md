![version](https://img.shields.io/badge/version-20%2B-E23089)
![platform](https://img.shields.io/static/v1?label=platform&message=mac-intel%20|%20mac-arm%20|%20win-64&color=blue)
[![license](https://img.shields.io/github/license/miyako/4d-plugin-get-localized-name)](LICENSE)
![downloads](https://img.shields.io/github/downloads/miyako/4d-plugin-get-localized-name/total)

# 4d-plugin-get-localized-name

The `Name` plugin returns the OS-localized display name, type description, and (on Windows) a link-overlay icon for a `4D.File` or `4D.Folder` object, by asking the host operating system's shell directly (Windows Shell API / macOS `NSURL` resource keys and Uniform Type Identifiers) rather than deriving them from the file's raw name or extension. The result is a plain `Object`, whose exact set of properties differs by platform and by what the OS is able to resolve for the given item.

| Command | Returns | Purpose |
|---|---|---|
| [`Get localized name`](#get-localized-name) | `Object` | Get the OS-localized name, type description, and (Windows only) link-overlay icon for a file or folder |

**Platforms:** Windows, macOS

---

## Requirements & platform notes

- **The parameter must be a `4D.File` or `4D.Folder` object.** Anything else (a plain object, a null/undefined parameter, a `4D.Folder`/`4D.File` for a path that no longer exists) is not an error — the command returns an empty object (`{}`) with no properties set. See [Error handling](#error-handling--troubleshooting).
- **The property set is not the same on both platforms.** Windows can return a `linkOverlayIcon` `Picture`; macOS never does. macOS can return `localizedLabel` (the Finder tag/label color name); Windows never does. `localizedDescription` and `localizedTypeDescription` exist on both platforms but come from different underlying OS mechanisms (see each property's note below).
- **Every property is populated independently and can be silently absent.** There is no single "success" or "failure" signal — each property is set only if its specific underlying OS call succeeds and returns a non-empty value. Always guard with `If ($result.property#Null)` before reading a property rather than assuming it's set.
- **On Windows**, resolving the link-overlay icon (`SHIL_JUMBO` via `SHGetImageList`) requires **Windows Vista or later**. The rest of the Windows properties (`AssocQueryString`, `SHGetFileInfo`) work on any Windows version 4D itself supports.
- **On macOS**, all properties are read through standard `NSURL` resource keys and Uniform Type Identifiers, both of which have been stable since early macOS 10.x; no specific minimum version is implied beyond whatever 4D itself requires.
- **This command is declared `threadSafe` in the plugin's manifest** — it can be called concurrently from multiple 4D processes/threads. On Windows, obtaining the shell's overlay-enabled icon list is now internally serialized by the plugin so concurrent calls don't race on that shared OS resource; you don't need to add your own locking around calls to this command.

---

## Get localized name

### Syntax

```4d
Get localized name ( item ) → Object
```

| Parameter | Type | Description |
|---|---|---|
| `item` | Object | A `4D.File` or `4D.Folder` object identifying the item to look up |
| Result | Object | The localized properties the OS could resolve for `item` — see below. Never `Null`; may be `{}` |

The result object's possible properties:

| Property | Type | Platform | Description |
|---|---|---|---|
| `localizedName` | Text | Both | The name shown by the OS shell (Explorer/Finder), which can differ from `item.name` — e.g. localized names for special/system folders. |
| `localizedTypeDescription` | Text | Both | The OS's human-readable type description (e.g. "Microsoft Excel Worksheet", "Application"). |
| `localizedDescription` | Text | Both | **On Windows**, the friendly document-type description from the file's registered file association (`AssocQueryString`/`ASSOCSTR_FRIENDLYDOCNAME`). **On macOS**, the description of the Uniform Type Identifier matching the item's file extension — only set if the item has an extension. |
| `localizedLabel` | Text | macOS only | The name of the Finder tag/label color applied to the item, if any. No Windows equivalent exists — this property is simply absent on Windows. |
| `linkOverlayIcon` | Picture | Windows only | A PNG-encoded jumbo icon for the item with the shell's shortcut/link overlay arrow composited onto it, sourced from the Windows shell's system image list. Not produced on macOS; this property is simply absent there. |

### Description

`item` must resolve to `4D.File` or `4D.Folder` — the command checks the object's runtime class (via `OB Class`) before doing anything else, so passing an object of a different class, or one that doesn't identify a real class at all, returns `{}` rather than raising a 4D error. It does not check whether the file/folder actually exists on disk; a `4D.File`/`4D.Folder` for a nonexistent path is passed straight through to the OS calls, which then typically fail their own checks and simply leave the corresponding properties unset.

**On Windows**, `localizedName` and `localizedTypeDescription` come from `SHGetFileInfo` and reflect exactly what Explorer would show; `localizedDescription` comes from the separate file-association lookup and can differ from `localizedTypeDescription` for the same file (association-based "friendly doc name" vs. the shell's own type string). `linkOverlayIcon` is only attempted if the shell can resolve a system icon index for the item at all; if it can't (e.g. certain virtual/special items), the property is simply absent — there's no partial or placeholder icon.

**On macOS**, all four possible properties are resolved independently through `NSURL` resource keys / Uniform Type Identifiers; a failure or `nil` result for any one of them (checked via `error:nil`, i.e. errors are not surfaced) just omits that property rather than affecting the others.

### Example

From the plugin's own test method (`test.4dm`):

```4d
//%attributes = {}
$file:=Folder:C1567(fk desktop folder:K87:19).file("Github Desktop.lnk")
$name:=Get localized name($file)

$icon:=$name.linkOverlayIcon
PICTURE PROPERTIES:C457($icon; $width; $height)
CONVERT PICTURE:C1002($icon; ".png")

WRITE PICTURE FILE:C680(System folder:C487(Desktop:K41:16)+"icon.png"; $icon)

SET PICTURE TO PASTEBOARD:C521($icon)

$folder:=Folder:C1567(fk desktop folder:K87:19)
$name:=Get localized name($folder)

$file:=Folder:C1567(fk desktop folder:K87:19).file("lib.xlsx")
$name:=Get localized name($file)

SET TEXT TO PASTEBOARD:C523(JSON Stringify:C1217($name))
```

Guarding against a platform-specific or entirely missing property before use:

```4d
$name:=Get localized name(File:C1566("/path/to/document.pdf"))

If ($name.linkOverlayIcon#Null)  // Windows only — never present on macOS
    $icon:=$name.linkOverlayIcon
End if 

$label:=String:C10($name.localizedDescription; ""; "no description available")
```

(To enumerate every property a result actually contains rather than test one at a time, use 4D's object-introspection commands — check your Language Reference for the exact one on your 4D version, since this varies across versions.)

Looking up a folder instead of a file — same command, same shape of result, just no file-association-based description on Windows for a folder (folders have no file association, so `localizedDescription` will typically be absent for them there):

```4d
$desktop:=Folder:C1567(fk desktop folder:K87:19)
$info:=Get localized name($desktop)
ALERT:C41($info.localizedName+" — "+$info.localizedTypeDescription)
```

---

## Error handling & troubleshooting

- **An unrecognized or missing `item` returns `{}`, not a 4D error.** If `item` isn't a `4D.File`/`4D.Folder` (or is a class the command doesn't recognize), you get an empty object back with no properties — always check for the properties you need rather than assuming the object is populated.
- **Every property can be independently absent, even for a valid, existing file.** There's no overall success/failure flag on the result — treat each property's presence as its own signal.
- **`linkOverlayIcon` never appears on macOS**, and **`localizedLabel` never appears on Windows** — these are platform-exclusive properties, not something that's "usually" missing on the other platform; don't build logic that expects them universally.
- **On Windows, `localizedDescription` for a folder is typically absent**, since it's sourced from a file-type association lookup that doesn't apply to folders.
- **On an unexpected internal error, the command returns `{}` rather than leaving 4D waiting indefinitely** — this depends on a fix made during this plugin's code-review pass (a local `try/catch` around the command's handler that guarantees a return is always sent). This is forward-looking: it's true of a build compiled from the reviewed/fixed source, not necessarily of every previously-built binary of this plugin.
- **`linkOverlayIcon` reliability on Windows also depends on the code-review fixes** (explicit `GdiplusStartup`/`GdiplusShutdown` at plugin load/unload) — a build predating that fix may intermittently fail to produce this property, or behave unpredictably, since GDI+ was previously being used without being explicitly initialized.

---

## Quick reference

```4d
$file:=File:C1566("/path/to/file.ext")
$info:=Get localized name($file)

$name:=$info.localizedName
$type:=$info.localizedTypeDescription
$desc:=String:C10($info.localizedDescription; "")

// Windows only
If ($info.linkOverlayIcon#Null)
    WRITE PICTURE FILE:C680(System folder:C487(Desktop:K41:16)+"icon.png"; $info.linkOverlayIcon)
End if 

// macOS only
If ($info.localizedLabel#Null)
    ALERT:C41($info.localizedLabel)
End if 
```
