import { Component, OnInit, Inject, Input } from "@angular/core";
import { Router, ActivatedRoute, ParamMap } from "@angular/router";
import { TableFoodService, TableFood,   } from '@hqhoangvuong/api-client-803868';
import { ThemeServiceService } from "../../../../../style-service/theme-service.service";
import { ToastrService } from "ngx-toastr";
import { HttpHeaders } from "@angular/common/http";

@Component({
  selector: "app-tablefood-update-ui-component",
  templateUrl: "./tablefood-update-ui.component.html",
  styleUrls: ["./tablefood-update-ui.component.scss"],
})
export class TableFoodUpdateUIComponent implements OnInit {
  idSelectedInput = '';
  idSelectedInputNumber: number;
  isDarkThemeSubscription: boolean = false;
  service: TableFoodService;
  item: TableFood;
  token: any;



  constructor(
    private themeService: ThemeServiceService,
    @Inject(TableFoodService) srv: TableFoodService,

    private toastr: ToastrService,
    private route: ActivatedRoute
  ) {
    this.token = localStorage.getItem("accessToken");
    srv.defaultHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: "Bearer " + this.token,
    });

    this.item = {} as TableFood;
    this.service = srv;

    this.checkTheme();
  }

  ngOnInit(): void {
    this.idSelectedInput = this.route.snapshot.paramMap.get("id");
    this.idSelectedInputNumber = (+ this.idSelectedInput);
    this.getItemById();
    this.ddlDataBinding();
  }

  getItemById() {
    this.service
      .apiTableFoodIdGet(this.idSelectedInputNumber)
      .subscribe((data) => {
        this.item = data;
      });
  }

  checkTheme() {
    this.themeService.getDarkTheme().subscribe((ok) => {
      this.isDarkThemeSubscription = ok;
    });
    if (localStorage.getItem("dark") == "true") {
      this.isDarkThemeSubscription = true;
    } else {
      this.isDarkThemeSubscription = false;
    }
  }

  ddlDataBinding(): void {
    
  }

  onUpdateItem() {
    this.service.apiTableFoodPut(this.item).subscribe(
      (data) => {
        this.toastr.success("Update successfully", "Notification");
      },
      (err) => {
        this.toastr.warning("Bad request", "Notification");
      }
    );
  }
}
