import { Component, Inject, OnInit } from "@angular/core";
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material/dialog";
import { DialogData } from "../../../account-table-ui/account-table-ui.component";
import { AccountService } from "@hqhoangvuong/api-client-803868";
@Component({
  selector: "app-account-delete-ui-dialog",
  templateUrl: "./account-delete-ui-dialog.component.html",
  styleUrls: ["./account-delete-ui-dialog.component.scss"],
})
export class AccountDeleteUIComponent implements OnInit {
  isConfirm: boolean = false;
  constructor(
    private dialogRef: MatDialogRef<AccountDeleteUIComponent>,
    @Inject(AccountService) service: AccountService,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {}

  ngOnInit(): void {}
  onDeleteEvent() {
    this.isConfirm = true;
    this.dialogRef.close({ data: this.isConfirm });
  }
}
