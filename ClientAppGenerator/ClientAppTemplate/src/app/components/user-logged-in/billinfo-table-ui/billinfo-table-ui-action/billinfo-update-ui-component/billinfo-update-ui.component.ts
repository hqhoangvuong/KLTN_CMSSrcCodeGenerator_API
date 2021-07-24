import { Component, OnInit, Inject, Input } from "@angular/core";
import { Router, ActivatedRoute, ParamMap } from "@angular/router";
import { BillInfoService, BillInfo, FoodService, BillService,  Food, Bill,  } from '@hqhoangvuong/api-client-803868';
import { ThemeServiceService } from "../../../../../style-service/theme-service.service";
import { ToastrService } from "ngx-toastr";
import { HttpHeaders } from "@angular/common/http";

@Component({
  selector: "app-billinfo-update-ui-component",
  templateUrl: "./billinfo-update-ui.component.html",
  styleUrls: ["./billinfo-update-ui.component.scss"],
})
export class BillInfoUpdateUIComponent implements OnInit {
  idSelectedInput = '';
  idSelectedInputNumber: number;
  isDarkThemeSubscription: boolean = false;
  service: BillInfoService;
  item: BillInfo;
  token: any;
  foodItems: Food[] = [];
  billItems: Bill[] = [];

  foodService: FoodService;
  billService: BillService;


  constructor(
    private themeService: ThemeServiceService,
    @Inject(BillInfoService) srv: BillInfoService,
    @Inject(FoodService) foodsrv:  FoodService,
    @Inject(BillService) billsrv:  BillService,

    private toastr: ToastrService,
    private route: ActivatedRoute
  ) {
    this.token = localStorage.getItem("accessToken");
    srv.defaultHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: "Bearer " + this.token,
    });
    foodsrv.defaultHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: "Bearer " + this.token,
    });
    billsrv.defaultHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: "Bearer " + this.token,
    });

    this.item = {} as BillInfo;
    this.service = srv;
    this.foodService = foodsrv;
    this.billService = billsrv;

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
      .apiBillInfoIdGet(this.idSelectedInputNumber)
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
        this.foodService.apiFoodGet().subscribe((result) => {
      this.foodItems = result;
    })
    this.billService.apiBillGet().subscribe((result) => {
      this.billItems = result;
    })

  }

  onUpdateItem() {
    /* OnUpdate
    this.service.apiBillInfoPut(this.item).subscribe(
      (data) => {
        this.toastr.success("Update successfully", "Notification");
      },
      (err) => {
        this.toastr.warning("Bad request", "Notification");
      }
    );
    OnUpdate */
  }
}
