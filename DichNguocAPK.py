from androguard.misc import AnalyzeAPK

a,d,dx = AnalyzeAPK('apk_test.apk')


# hiển thị các activity
a1 = str(a.get_activities())
print(a1)

# hiển thị các permission
a2 = str(a.get_permissions())
print(a2)

a3 = str(a.get_android_manifest_axml().get_xml())
print (a3)

a5 = str(a.get_android_manifest_xml())
print(a5)

a6 = str(a.get_package())
print (a6)

a7 = str(a.get_app_name())
print(a7)

a8 = str(a.get_app_icon())
print (a8)

a9 = str(a.get_androidversion_code())
print (a9)

a10 = str(a.get_androidversion_name())
print(a10)

a11 = str(a.get_min_sdk_version())
print (a11)

a12 = str(a.get_max_sdk_version())
print(a12)

a13 = str(a.get_target_sdk_version())
print (a13)

a14 = str(a.get_effective_target_sdk_version())
print(a14)

# Tao file txt de su dung cho RF
A = a1 + a2 + a3
print(A)

with open('log.txt', 'w') as w:
			w.write(A)


