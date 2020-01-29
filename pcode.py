import os, shell
def refresh(gitPath, brash, savePath):
	if os.path.exists(savePath):
		cmd = "git clone -b %s --depth=1 %s %s"%(brash, gitPath, savePath)
	else:
		cmd = "cd %s;git pull"%(savePath)
		shell.run(cmd)
	