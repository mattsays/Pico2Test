const std = @import("std");

// Although this function looks imperative, note that its job is to
// declaratively construct a build graph that will be executed by an external
// runner.
pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const package = b.dependency("zant", .{
        .target = target,
        .optimize = optimize,
    });
    const tensor_module = package.module("tensor");
    const model_import_export_module = package.module("model_import_export");

    const lib = b.addStaticLibrary(.{
        .name = "neural_network",
        // In this case the main source file is merely a path, however, in more
        // complicated build scripts, this could be a generated file.
        .root_source_file = b.path("src/lib.zig"),
        .target = target,
        .optimize = optimize,
    });

    lib.root_module.addImport("tensor", tensor_module);
    lib.root_module.addImport("model_import_export", model_import_export_module);

    // This declares intent for the library to be installed into the standard
    // location when the user invokes the "install" step (the default step when
    // running `zig build`).
    const install_lib_step = b.addInstallArtifact(lib, .{});

    const lib_step = b.step("lib", "Compile static library");
    lib_step.dependOn(&install_lib_step.step);
}
