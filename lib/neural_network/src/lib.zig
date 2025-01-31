const std = @import("std");
const tensor = @import("tensor");
const model_import_export = @import("model_import_export");
const build_options = @import("build_options");

pub const std_options = .{
    // Set the log level to info
    .log_level = .info,

    // Define logFn to override the std implementation
    .logFn = customLogFn,
};

var log_function: ?*const fn (string: [*]const u8) callconv(.C) void = null;

pub fn customLogFn(
    comptime level: std.log.Level,
    comptime scope: @Type(.EnumLiteral),
    comptime format: []const u8,
    args: anytype,
) void {
    _ = level;
    _ = scope;
    if (log_function) |unwrapped_log_function| {
        var buf: [256]u8 = [_]u8{0} ** 256;
        unwrapped_log_function((std.fmt.bufPrint(buf[0..250], format, args) catch return).ptr);
    }
}

export fn setLogFunction(function: *const fn (string: [*]const u8) callconv(.C) void) void {
    log_function = function;
}

export fn predict(input: *anyopaque, output: *anyopaque) i16 {
    _ = input;
    _ = output;

    std.log.info("Zant ready!", .{});

    return 0;
}
