##!/bin/sh
##### Input Params Set
# 工程名
project_name=$1
# workspace工作目录
workspace=$2
# 编译模式
build_type=2

git_path=$3

project_scheme=$project_name
echo "工程名: $project_name, 工作目录: $workspace, 编译模式: build_type"

#### Output Params Set


# 代码路径
project_path=$workspace/$project_name
# 项目xcarchive路径
archive_path=$workspace/$project_name.xcarchive
project_workspace=$project_path/$project_name.xcworkspace
# ipa文件存放路径
export_ipa_path=$workspace/

# exportOptions plist 
export_options_plist="abc.plist"
if [[ $build_type == 1 ]]; then
    build_type=Release
    export_options_plist=./appstore.plist
elif [[ $build_type == 2 ]]; then
    build_type=Release
    export_options_plist=./adhoc.plist
else
    build_type=Debug
    export_options_plist=./dev.plist
fi

codepath=$project_workspace/$project_name
# rm -rf $project_workspace/$project_name
if [ ! -d $codepath ];then
	echo "///-----------"
	echo "/// 正在下载工程代码"
	echo "///-----------"
	git clone -b dev --depth=1 git_path $codepath
	cd $codepath
	echo "///-----------"
	echo "/// 正在更新Pod"
	echo "///-----------"
	pod install --no-repo-update
else
    cd $codepath
    git pull
fi

echo "///-----------"
echo "/// 正在清理工程"
echo "///-----------"
xcodebuild clean -workspace $project_workspace -scheme $project_scheme -configuration $build_type -quiet || exit


echo "///-----------"
echo "/// 正在编译工程: ${build_type}"
echo "///-----------"
xcodebuild archive -workspace ${project_workspace} -scheme ${project_scheme} -configuration $build_type -archivePath $archive_path || exit

echo "///-----------"
echo "/// 开始导出ipa: ${export_ipa_path}"
echo "///-----------"
xcodebuild -exportArchive -archivePath $archive_path -exportPath ${export_ipa_path} -exportOptionsPlist ${export_options_plist} -quiet || exit

if [[ -e $export_ipa_path/$project_scheme.ipa ]]; then
    echo "///-----------"
    echo "/// ipa包已导出"
    echo "///-----------"
    open $export_ipa_path
fi

echo "///-----------"
echo "/// 开始导出dSYM: ${export_ipa_path}"
echo "///-----------"
cp -r $workspace/$project_name.xcarchive/dSYMs/${project_name}.app.dSYM $workspace
zip -r -o $workspace/$project_name.app.dSYM.zip $workspace/${project_name}.app.dSYM

if [[ -e $workspace/$project_name.app.dSYM.zip ]]; then
    echo "///-----------"
    echo "/// dSYM已导出"
    echo "///-----------"
    open $export_ipa_path
fi


echo "///-----------"
echo "/// 开始导出symbol: ${export_ipa_path}"
echo "///-----------"
cp -r $workspace/$project_name.xcarchive/BCSymbolMaps $workspace
zip -r -o $workspace/symbol.zip $workspace/BCSymbolMaps

if [[ -e $workspace/symbol.zip ]]; then
    echo "///-----------"
    echo "/// symbol已导出"
    echo "///-----------"
    open $export_ipa_path
fi

exit
echo "///-----------"
echo "/// 正在上传至Fir"
echo "///-----------"
fir login -T ac21ca5a5fd1c83646352b6eb6e392ec
fir publish $export_ipa_path/$project_scheme.ipa


# echo "///-----------"
# echo "/// 正在上传至AppStore"
# echo "///-----------"
#xcrun altool --validate-app -f $export_ipa_path/$project_scheme.ipa -t ios --apiKey '9K86F595RP' --apiIssuer '658486a8-330e-429b-ae36-bbab7bbfe596' --verbose
#xcrun altool --upload-app -f $export_ipa_path/$project_scheme.ipa -t ios --apiKey '9K86F595RP' --apiIssuer '658486a8-330e-429b-ae36-bbab7bbfe596' --verbose

#Bugly
#设置项目版本号
bundle_short_version=$(/usr/libexec/PlistBuddy -c "Print CFBundleShortVersionString" ${project_path}/${project_name}/Info.plist)
bundle_version=$(/usr/libexec/PlistBuddy -c "Print CFBundleVersion" ${project_path}/${project_name}/Info.plist)
echo $bundle_short_version
echo $bundle_version

buglyAppKey="xx"
buglyAppId="xx"
bundleId="com.xxx.xxxx"

echo "///-----------"
echo "/// 正在上传dysm至Bugly"
echo "///-----------"
curl -k "https://api.bugly.qq.com/openapi/file/upload/symbol?app_key=$buglyAppKey&app_id=$buglyAppId" --form "api_version=1" --form "app_id=$buglyAppId" --form "app_key=$buglyAppKey" --form "symbolType=2"  --form "bundleId=${bundleId}" --form "productVersion=${bundle_short_version}(${bundle_version})" --form "channel=appstore" --form "fileName=$project_name.app.dSYM.zip" --form "file=@$workspace/$project_name.app.dSYM.zip" --verbose
echo "///-----------"
echo "/// 上传dysm至Bugly成功"
echo "///-----------"

echo "///-----------"
echo "/// 正在上传symbol至Bugly"
echo "///-----------"
curl -k "https://api.bugly.qq.com/openapi/file/upload/symbol?app_key=$buglyAppKey&app_id=$buglyAppId" --form "api_version=1" --form "app_id=$buglyAppId" --form "app_key=$buglyAppKey" --form "symbolType=2"  --form "bundleId=${bundleId}" --form "productVersion=${bundle_short_version}(${bundle_version})" --form "fileName=symbol.zip" --form "file=@$workspace/$project_name.xcarchive/symbol.zip" --verbose
echo "///-----------"
echo "/// 上传symbol至Bugly成功"
echo "///-----------"


