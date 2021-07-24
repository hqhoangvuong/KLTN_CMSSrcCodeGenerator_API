#!/bin/bash
cd /root/CustomerAPIGenerate/EFCoreScaffold
dotnet ef dbcontext scaffold "Server="$1";Port="$6";Database="$2";Persist Security Info=True;User ID="$3";Password="$4"" Pomelo.EntityFrameworkCore.MySql -d -o "$5"