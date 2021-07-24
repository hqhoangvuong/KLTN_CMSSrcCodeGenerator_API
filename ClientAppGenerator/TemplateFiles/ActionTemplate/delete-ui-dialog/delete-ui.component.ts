import { Component, Inject, OnInit } from "@angular/core";
import { MatDialogRef, MAT_DIALOG_DATA } from "@angular/material/dialog";
import { DialogData } from "../../../[--TableUIComponentPath--]";
import { [--ServiceName--] } from "[--ApiClientPackageId--]";
@Component({
  selector: "[--SelectorName--]",
  templateUrl: "./[--UrlName--].html",
  styleUrls: ["./[--UrlName--].scss"],
})
export class [--ClassName--] implements OnInit {
  isConfirm: boolean = false;
  constructor(
    private dialogRef: MatDialogRef<[--ClassName--]>,
    @Inject([--ServiceName--]) service: [--ServiceName--],
    @Inject(MAT_DIALOG_DATA) public data: DialogData
  ) {}

  ngOnInit(): void {}
  onDeleteEvent() {
    this.isConfirm = true;
    this.dialogRef.close({ data: this.isConfirm });
  }
}
