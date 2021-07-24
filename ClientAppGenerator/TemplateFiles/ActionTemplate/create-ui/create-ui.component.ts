import { Component, Inject, OnInit } from "@angular/core";
import { Router } from '@angular/router';
import { ThemeServiceService } from '../../../../../style-service/theme-service.service';
import { [--ServiceName--], [--ModelName--], [--FKServiceName--] [--FKModelName--] } from '[--ApiClientPackageId--]';
import { HttpHeaders } from "@angular/common/http";
import { ToastrService } from "ngx-toastr";

@Component({
  selector: "[--SelectorName--]",
  templateUrl: "./[--UrlName--].html",
  styleUrls: ["./[--UrlName--].scss"],
})

export class [--ClassName--] implements OnInit {
  isDarkThemeSubscription: boolean = false;
  entityDisplayName = "Create";
  isContinueToCreate: boolean = true;
  service: [--ServiceName--];
  item: [--ModelName--];
[--FKItems--]
[--FKServices--]
  itemSeleted: any;
  token: any;

  constructor(
    private themeSerive: ThemeServiceService,
    private route: Router,
    @Inject([--ServiceName--]) srv: [--ServiceName--],
[--InjectFK--]
    private toast: ToastrService
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
[--FKDataBinding--]
  }

  createNewItem() {
    /* CreateLogicSession
    this.service.api[--ModelName--]Post(this.item).subscribe(
      (data) => {
        this.toast.success("Create new [--ExplicitName--] successfully", "Information");
      },
      (err) => {
        this.toast.warning("Something wrong happen", "Warning");
      }
    );

    if (!this.isContinueToCreate) {
      this.route.navigate(['/user/index/[--LowerModelName--]management']);
    }
    CreateLogicSession */
  }
}
