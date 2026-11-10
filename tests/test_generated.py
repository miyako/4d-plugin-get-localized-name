"""The final publication exemption is smaller than the bundle or build roots."""

import unittest

from helper_support import source
import native


class GeneratedOutputTests(unittest.TestCase):
    def test_exact_native_files_and_controlled_directory_descendants(self):
        expected = (
            "test/Plugins/Name.bundle/Contents/MacOS/Name",
            "test/Plugins/Name.bundle/Contents/Info.plist",
            "test/Plugins/Name.bundle/Contents/Resources/English.lproj/InfoPlist.strings",
            "test/Plugins/Name.bundle/Contents/_CodeSignature/CodeResources",
            "test/Plugins/Name.bundle/Contents/Resources/constants.xlf",
            "test/Plugins/Name.bundle/Contents/Resources/manifest.json",
            "build/XCBuildData/build.db",
            "build/XCBuildData/build.db-wal",
            "build/XCBuildData/build.db-shm",
            "build/XCBuildData/0123456789abcdef0123456789abcdef.xcbuilddata/build-request.json",
            "build/Name.build/Objects-normal/arm64/main.o",
            "build/Default/Name.build/build.db",
            "test/Plugins/Name.build/Objects/file.o",
            "test/Plugins/Default/Name.build/Objects/file.o",
            "test/Plugins/Name.bundle/Contents/Windows64/Name.4DX",
            *(str(path) for path in native.DOWNLOADS),
        )
        for path in expected:
            with self.subTest(path=path):
                self.assertTrue(native.generated(path))

    def test_every_resource_source_or_unproven_output_stays_protected(self):
        excluded = (
            "test/Plugins/Name.bundle/Contents/Windows/Name.4DX",
            "test/Plugins/Name.bundle/Contents/MacOS/runtime.dylib",
            "test/Plugins/Name.bundle/Contents/QuickLook/Thumbnail.png",
            "test/Plugins/Default/Name.bundle/Contents/Info.plist",
            "test/Plugins/Default/keep", "build/XCBuildData-evil/build.db",
            "build/unexpected-source.cpp",
            "build/XCBuildData/unexpected-source.cpp",
            "build/XCBuildData/build.db-evil",
            "build/XCBuildData/evil.xcbuilddata/build-request.json",
            "build/Name.build-evil/injected.cpp",
            "test/Plugins/Name.bundle/Contents/_CodeSignature-evil/file",
            "test/Plugins/Name.bundle/Contents/Info.plist.backup",
            *map(str, source.SOURCE_PATHS),
        )
        for path in excluded:
            with self.subTest(path=path):
                self.assertFalse(native.generated(path))
