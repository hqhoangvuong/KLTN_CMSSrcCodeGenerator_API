import { Component, Input, OnInit, Inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { SystemLogService, SystemLog } from '@hqhoangvuong/api-client-803868';
import { ThemeServiceService } from '../../../../../style-service/theme-service.service';

@Component({
  selector: "app-systemlog-read-ui-component",
  templateUrl: "./systemlog-read-ui.component.html",
  styleUrls: ["./systemlog-read-ui.component.scss"],
})

export class SystemLogReadUIComponent implements OnInit {
  service: SystemLogService;
  isDarkThemeSubscription: boolean=false;
  item: SystemLog;
  idSelectedInput = '';
  idSelectedInputNumber: number;
  constructor(private themeService: ThemeServiceService,
    @Inject(SystemLogService) srv: SystemLogService,
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
    this.service.apiSystemLogIdGet(this.idSelectedInputNumber).subscribe(data => {
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
