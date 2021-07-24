import { Component, Inject, OnInit } from "@angular/core";
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material/dialog";
import { DialogData } from "../../../tablefood-table-ui/tablefood-table-ui.component";
import { TableFoodService } from "@hqhoangvuong/api-client-803868";
@Component({
  selector: "app-tablefood-delete-ui-dialog",
  templateUrl: "./tablefood-delete-ui-dialog.component.html",
  styleUrls: ["./tablefood-delete-ui-dialog.component.scss"],
})
export class TableFoodDeleteUIComponent implements OnInit {
  isConfirm: boolean = false;
  constructor(
    private dialogRef: MatDialogRef<TableFoodDeleteUIComponent>,
    @Inject(TableFoodService) service: TableFoodService,
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {}

  ngOnInit(): void {}
  onDeleteEvent() {
    this.isConfirm = true;
    this.dialogRef.close({ data: this.isConfirm });
  }
}
