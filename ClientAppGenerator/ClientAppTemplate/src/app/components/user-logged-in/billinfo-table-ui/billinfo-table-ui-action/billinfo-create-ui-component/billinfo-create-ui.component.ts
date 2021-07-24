import { Component, Inject, OnInit } from "@angular/core";
import { Router } from '@angular/router';
import { ThemeServiceService } from '../../../../../style-service/theme-service.service';
import { BillInfoService, BillInfo, FoodService, BillService,  Food, Bill,  } from '@hqhoangvuong/api-client-803868';
import { HttpHeaders } from "@angular/common/http";
import { ToastrService } from "ngx-toastr";

@Component({
  selector: "app-billinfo-create-ui-component",
  templateUrl: "./billinfo-create-ui.component.html",
  styleUrls: ["./billinfo-create-ui.component.scss"],
})

export class BillInfocreateUIComponent implements OnInit {
  isDarkThemeSubscription: boolean = false;
  entityDisplayName = "Create";
  isContinueToCreate: boolean = true;
  service: BillInfoService;
  item: BillInfo;
  foodItems: Food[] = [];
  billItems: Bill[] = [];

  foodService: FoodService;
  billService: BillService;

  itemSeleted: any;
  token: any;

  constructor(
    private themeSerive: ThemeServiceService,
    private route: Router,
    @Inject(BillInfoService) srv: BillInfoService,
    @Inject(FoodService) foodsrv:  FoodService,
    @Inject(BillService) billsrv:  BillService,

    private toast: ToastrService
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

  checkTheme() {
    this.themeSerive.getDarkTheme().subscribe((ok) => {
      this.isDarkThemeSubscription = ok;
    });
    if (localStorage.getItem("dark") == "true") {
      this.isDarkThemeSubscription = true;
    } else {
      this.isDarkThemeSubscription = false;
    }
  }

  ngOnInit(): void {
    this.ddlDataBinding();
  }

  ddlDataBinding(): void {
    this.foodService.apiFoodGet().subscribe((result) => {
      this.foodItems = result;
    })
    this.billService.apiBillGet().subscribe((result) => {
      this.billItems = result;
    })

  }

  createNewItem() {
    /* CreateLogicSession
    this.service.apiBillInfoPost(this.item).subscribe(
      (data) => {
        this.toast.success("Create new Bill Info  successfully", "Information");
      },
      (err) => {
        this.toast.warning("Something wrong happen", "Warning");
      }
    );

    if (!this.isContinueToCreate) {
      this.route.navigate(['/user/index/billinfomanagement']);
    }
    CreateLogicSession */
  }
}
