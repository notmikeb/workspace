
## prepare git_server

dos>mkdir o:\git_server
dos>cd git_server
dos>git init --bare myapp2
dos>git init --bare myapp2.sdk
dos>git init --bare myapp2.case


## want to use repo.cmd to build-up a archive

root
|
|_ myapp2
|  |
|  +--myapp_sdk
|  +--myapp_case
|_ README.md


## a default.xml inside the root folder of myapp2

origin -> the remote's name

```
<?xml version="1.0" encoding="UTF-8"?>
<manifest>
  <remote  name="origin"
           fetch=".."
           review="https://android-review.googlesource.com/" />
  <default revision="master"
           remote="origin"
           sync-j="4" />
  <project path="myapp2/myapp_case" name="myapp2.case" groups="pdk" >
    <copyfile src="txt/readme.md" dest="README.md" />
  </project>
  <project path="myapp2/myapp_sdk" name="myapp2.sdk" groups="pdk,tradefed" />
  
</manifest>
```


## download with repo

set repo.cmd to dos path
dos>mkdir newfolder
dos>cd newfolder
dos>repo init -u o:\git_server\myapp2

it will download the myapp2 repository and check its default.xml
Use default.xml's structure to git more repositories