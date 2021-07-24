import { Component, OnInit, Inject, Input } from "@angular/core";
import { Router, ActivatedRoute, ParamMap } from "@angular/router";
import { BillService, Bill, TableFoodService,  TableFood,  } from '@hqhoangvuong/api-client-803868';
import { ThemeServiceService } from "../../../../../style-service/theme-service.service";
import { ToastrService } from "ngx-toastr";
import { HttpHeaders } from "@angular/common/http";

@Component({
  selector: "app-bill-update-ui-component",
  templateUrl: "./bill-update-ui.component.html",
  styleUrls: ["./bill-update-ui.component.scss"],
})
export class BillUpdateUIComponent implements OnInit {
  idSelectedInput = '';
  idSelectedInputNumber: number;
  isDarkThemeSubscription: boolean = false;
  service: BillService;
  item: Bill;
  token: any;
  tableFoodItems: TableFood[] = [];

  tableFoodService: TableFoodService;


  constructor(
    private themeService: ThemeServiceService,
    @Inject(BillService) srv: BillService,
    @Inject(TableFoodService) tableFoodsrv:  TableFoodService,

    private toastr: ToastrService,
    private route: ActivatedRoute
  ) {
    this.token = localStorage.getItem("accessToken");
    srv.defaultHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: "Bearer " + this.token,
    });
    tableFoodsrv.defaultHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: "Bearer " + this.token,
    });

    this.item = {} as Bill;
    this.service = srv;
    this.tableFoodService = tableFoodsrv;

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
      .apiBillIdGet(this.idSelectedInputNumber)
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
        this.tableFoodService.apiTableFoodGet().subscribe((result) => {
      this.tableFoodItems = result;
    })

  }

  onUpdateItem() {
    this.service.apiBillPut(this.item).subscribe(
      (data) => {
        this.toastr.success("Update successfully", "Notification");
      },
      (err) => {
        this.toastr.warning("Bad request", "Notification");
      }
    );
  }
}
