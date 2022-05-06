from types import SimpleNamespace
PoppinsFiles = {
    'Regular': './fonts/Poppins_Font_2/Poppins-Regular.ttf',
    'SemiBold': './fonts/Poppins_Font_2/Poppins-SemiBold.ttf',
}
PoppinsFont = SimpleNamespace(**PoppinsFiles)
print(f"Poppins.Regular: {PoppinsFont.Regular}")
# eof
