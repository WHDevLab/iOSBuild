#coding=utf-8
import shell
import os

projectName="Wechat"


def clean(workspace, scheme):
	cmd = "xcodebuild clean -workspace %s -scheme %s -configuration $build_type -quiet || exit"%(workspace, scheme)
	shell.run(cmd)

def archive(workspace, scheme, build_type, archive_path):
	cmd = "xcodebuild archive -workspace %s -scheme %s -configuration %s -archivePath %s || exit"%(workspace, scheme, build_type, archive_path)
	shell.run(cmd)

def exportIpa(archivePath, export_ipa_path, export_options_plist):
	cmd = "xcodebuild -exportArchive -archivePath %s -exportPath %s -exportOptionsPlist %s -quiet || exit"%(archivePath, export_ipa_path, export_options_plist)
	shell.run(cmd)

def exportDYSM(archivePath):
	workspace=os.path.dirname(archivePath)
	project_name=os.path.splitext(os.path.basename(archivePath))[0]

	dysmZipPath = workspace+"/"+project_name+".app.dSYM.zip"
	dysmPath = workspace+"/"+project_name+".app.dSYM"
	shell.run("cp -r %s/dSYMs/%s.app.dSYM %s"%(archivePath, project_name, workspace))
	shell.run("zip -r -o %s %s"%(dysmZipPath, dysmPath))

def exportSymbol(archivePath):
	workspace=os.path.dirname(archivePath)
	project_name=os.path.splitext(os.path.basename(archivePath))[0]

	symbolZipPath = workspace+"/"+project_name+".app.dSYM.zip"
	symbolPath = workspace+"/"+"BCSymbolMaps"

	shell.run("cp -r %s/BCSymbolMaps %s"%(archivePath, workspace))
	shell.run("zip -r -o %s %s"%(symbolZipPath, symbolPath))

def run():
	#xcarchive导出路径
	archivePath = "/Users/design/Desktop/dabao/%s.xcarchive"%projectName
	#参数：xcarchive文件路径，导出ipa存储路径，签名配置文件路径(每次使用xcode打包之后会生成)
	exportIpa(archivePath, "/Users/design/Desktop/dabao/ipa", "./adhoc.plist")
	#dysm(bug分析定位) 所在路径
	exportDYSM("/Users/design/Desktop/dabao/%s.xcarchive"%projectName)
	#符号表(bug分析定位) 所在路径
	exportSymbol("/Users/design/Desktop/dabao/%s.xcarchive"%projectName)
	

