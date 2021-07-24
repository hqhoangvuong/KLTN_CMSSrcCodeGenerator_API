import { Component, Inject, OnInit } from "@angular/core";
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material/dialog";
import { DialogData } from "../../../bill-table-ui/bill-table-ui.component";
import { BillService } from "@hqhoangvuong/api-client-803868";
@Component({
  selector: "app-bill-delete-ui-dialog",
  templateUrl: "./bill-delete-ui-dialog.component.html",
  styleUrls: ["./bill-delete-ui-dialog.component.scss"],
})
export class BillDeleteUIComponent implements OnInit {
  isConfirm: boolean = false;
  constructor(
    private dialogRef: MatDialogRef<BillDeleteUIComponent>,
    @Inject(BillService) service: BillService,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {}

  ngOnInit(): void {}
  onDeleteEvent() {
    this.isConfirm = true;
    this.dialogRef.close({ data: this.isConfirm });
  }
}
