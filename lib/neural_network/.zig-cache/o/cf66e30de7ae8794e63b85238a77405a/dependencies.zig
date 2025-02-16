pub const packages = struct {
    pub const @"122035d604c67bac65ebde118a9d16136edf74a98ee0dbaddf0f6576c417d0a54620" = struct {
        pub const build_root = "/home/marco/pi-pico-zant/lib/neural_network/../Z-Ant";
        pub const build_zig = @import("122035d604c67bac65ebde118a9d16136edf74a98ee0dbaddf0f6576c417d0a54620");
        pub const deps: []const struct { []const u8, []const u8 } = &.{
        };
    };
};

pub const root_deps: []const struct { []const u8, []const u8 } = &.{
    .{ "zant", "122035d604c67bac65ebde118a9d16136edf74a98ee0dbaddf0f6576c417d0a54620" },
};
