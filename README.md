# 4d-plugin-get-localized-name


### macOS

```4d
$folder:=Folder(fk desktop folder)
$name:=Get localized name($folder)
```

```json
{"localizedName":"デスクトップ"}
```

```4d
$file:=Folder(fk desktop folder).file("spreadsheet.xlsx")
$name:=Get localized name($file)
```

```json
{"localizedName":"lib.xlsx","localizedTypeDescription":"Microsoft Excel Workbook (.xlsx)","localizedDescription":"Office Open XMLスプレッドシート"}
```

