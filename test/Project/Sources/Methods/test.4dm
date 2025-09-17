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