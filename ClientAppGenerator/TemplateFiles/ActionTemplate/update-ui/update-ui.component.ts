import { Component, OnInit, Inject, Input } from "@angular/core";
import { Router, ActivatedRoute, ParamMap } from "@angular/router";
import { [--ServiceName--], [--ModelName--], [--FKServiceName--] [--FKModelName--] } from '[--ApiClientPackageId--]';
import { ThemeServiceService } from "../../../../../style-service/theme-service.service";
import { ToastrService } from "ngx-toastr";
import { HttpHeaders } from "@angular/common/http";

@Component({
  selector: "[--SelectorName--]",
  templateUrl: "./[--UrlName--].html",
  styleUrls: ["./[--UrlName--].scss"],
})
export class [--ClassName--] implements OnInit {
  idSelectedInput = '';
  idSelectedInputNumber: number;
  isDarkThemeSubscription: boolean = false;
  service: [--ServiceName--];
  item: [--ModelName--];
  token: any;
[--FKItems--]
[--FKServices--]

  constructor(
    private themeService: ThemeServiceService,
    @Inject([--ServiceName--]) srv: [--ServiceName--],
[--InjectFK--]
    private toastr: ToastrService,
    private route: ActivatedRoute
  ) {
    this.token = localStorage.getItem("accessToken");
    srv.defaultHeaders = new HttpHeaders({
      "Content-Type": "application/json",
      Authorization: "Bearer " + this.token,
    });
[--FKServiceSetAuth--]
    this.item = {} as [--ModelName--];
    this.service = srv;
[---FKServiceInit--]
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
      .api[--ModelName--]IdGet([--CastedIdSelectInput--])
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
    [--FKDataBinding--]
  }

  onUpdateItem() {
    /* OnUpdate
    this.service.api[--ModelName--]Put(this.item).subscribe(
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
