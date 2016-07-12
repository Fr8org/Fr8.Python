param(
	[Parameter(Mandatory = $true)]
	[string]$gitRepo
)

$deploymentDir = "deployment"
$terminalDir = "terminalTwitter"
$sdkDirName = "fr8"
$sdkDir = "../$sdkDirName"

If (Test-Path $deploymentDir){
	Write-Host "Removing old $deploymentDir folder"
	Remove-Item $deploymentDir -Force -Recurse
}

Write-Host "Creating blank $deploymentDir folder"
New-Item -ItemType Directory -Force -Path $deploymentDir | Out-Null

Write-Host "Extracting current Azure repo"
cd $deploymentDir
git init
git remote add azure $gitRepo
git fetch azure
git checkout master
cd ..

Write-Host "Remove previous deployment"
Remove-Item "$deploymentDir\*" -Recurse

Write-Host "Creating terminal package"
Copy-Item "web.2.7.config" -Destination "$deploymentDir\web.config" -Force
Copy-Item "runtime.txt" -Destination $deploymentDir -Force
Copy-Item "requirements.txt" -Destination $deploymentDir -Force
Copy-Item "ptvs_virtualenv_proxy.py" -Destination $deploymentDir -Force
Copy-Item "runserver.py" -Destination $deploymentDir -Force
Copy-Item $terminalDir -Destination $deploymentDir -Force -Recurse
Remove-Item "$deploymentDir\$terminalDir\*.pyc" -Recurse

Write-Host "Creating SDK package for the terminal"
Copy-Item $sdkDir -Destination $deploymentDir -Force -Recurse
Remove-Item "$deploymentDir\$sdkDirName\*.pyc" -Recurse
Remove-Item "$deploymentDir\$sdkDirName\*.pyproj" -Recurse

Write-Host "Publishing to Azure Git repo"
cd $deploymentDir
git add .
git commit -m "Deployment commit"
git push azure master

cd ..
