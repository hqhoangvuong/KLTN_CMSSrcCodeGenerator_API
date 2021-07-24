import { Component, Input, OnInit, Inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BillService, Bill } from '@hqhoangvuong/api-client-803868';
import { ThemeServiceService } from '../../../../../style-service/theme-service.service';

@Component({
  selector: "app-bill-read-ui-component",
  templateUrl: "./bill-read-ui.component.html",
  styleUrls: ["./bill-read-ui.component.scss"],
})

export class BillReadUIComponent implements OnInit {
  service: BillService;
  isDarkThemeSubscription: boolean=false;
  item: Bill;
  idSelectedInput = '';
  idSelectedInputNumber: number;
  constructor(private themeService: ThemeServiceService,
    @Inject(BillService) srv: BillService,
    private route: ActivatedRoute) {
    this.service = srv;
    this.checkTheme();
    this.idSelectedInputNumber = -1;
  }

  ngOnInit(): void {
    this.idSelectedInput = this.route.snapshot.paramMap.get('id');
    this.idSelectedInputNumber = (+ this.idSelectedInput);
    this.getItemById();
  }

  getItemById() {
    this.service.apiBillIdGet(this.idSelectedInputNumber).subscribe(data => {
      this.item = data;
    })
  }

  checkTheme() {
    this.themeService.getDarkTheme().subscribe((ok) => {
      this.isDarkThemeSubscription = ok;
    });
    if (localStorage.getItem('dark') == 'true') {
      this.isDarkThemeSubscription = true;
    } else {
      this.isDarkThemeSubscription = false;
    }
  }
}
