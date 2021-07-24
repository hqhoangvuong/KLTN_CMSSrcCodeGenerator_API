#!/bin/bash
cd /root/CustomerAPIGenerate/EFCoreScaffold
dotnet ef dbcontext scaffold "Server="$1","$6";Database="$2";Persist Security Info=True;User ID="$3";Password="$4"" Microsoft.EntityFrameworkCore.SqlServer -d -o "$5"