path = r"C:\Users\irfan\AppData\Local\Pub\Cache\hosted\pub.dev\file_picker-4.6.1\android\build.gradle"
with open(path) as f:
    c = f.read()
c = c.replace("android {", "android {\n    namespace \"com.mr.flutter.plugin.filepicker\"", 1)
with open(path, "w") as f:
    f.write(c)
print("Done!")
