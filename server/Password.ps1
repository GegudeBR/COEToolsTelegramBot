param($ComputerName)

Import-Module AdmPwd.PS
Push-Location $PSScriptRoot # Change directory to script directory


if($ComputerName -eq $null) {
	$ComputerName = Read-Host "Computer name"
}

if (!(Get-ADComputer -Filter {name -eq $ComputerName})) {
	Write-Host "Invalid hostname!"
	Exit
}

# Setting Custom Password
$Encrypted = Get-Content SecureString.txt
$Secure_Password = ConvertTo-SecureString $Encrypted

$NewSession = New-PSSession -ComputerName $ComputerName
Enter-PSSession -Session $NewSession
Invoke-Command -Session $NewSession -ArgumentList $Secure_Password -ScriptBlock{
	param($Secure_Password)
	$UserAccount = Get-LocalUser -Name "Administrator"
	$UserAccount | Set-LocalUser -Password $Secure_Password
}
Exit-PSSession
Write-Host "Custom Password Set"

# Wait
Start-Sleep -Seconds 30
# Resetting LAPS Password 
$ExpireTime = Get-Date
$ExpireTime.AddMinutes(-5)
Reset-AdmPwdPassword -ComputerName $ComputerName -WhenEffective $ExpireTime

# Propagating Change
Invoke-GPUpdate -Computer $ComputerName -RandomDelayInMinutes 0 -Force

Enter-PSSession -Session $NewSession
Invoke-Command -Session $NewSession -ArgumentList $Secure_Password -ScriptBlock{
	Invoke-GPUpdate -RandomDelayInMinutes 0 -Force
}
Exit-PSSession

Write-Host "LAPS Password Set"
Remove-PSSession -Session $NewSession



