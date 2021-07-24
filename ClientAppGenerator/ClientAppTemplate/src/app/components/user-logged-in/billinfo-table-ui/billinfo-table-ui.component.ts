import {
  Component,
  OnInit,
  Output,
  EventEmitter,
  HostListener,
  Inject,
} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { PageEvent } from '@angular/material/paginator';
import { ThemeServiceService } from '../../../style-service/theme-service.service';
import { ToastrService } from 'ngx-toastr';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BillInfoService, BillInfo } from '@hqhoangvuong/api-client-803868';

@Component({
  selector: 'app-billinfo-table-ui',
  templateUrl: './billinfo-table-ui.component.html',
  styleUrls: ['./billinfo-table-ui.component.scss'],
})

export class BillInfoTableUIComponent implements OnInit {
  _service: BillInfoService;
  modelDisplayName: string;
  listItems: BillInfo[] = [];
  @Output() nameActionTrigger = new EventEmitter<any>();
  contentType: string[] = ['text/html', 'charset=UTF-8'];
  pageIndex: number = 1;
  pageSize: number = 10;
  pageDataTotalCount: number;
  pageEvent: PageEvent;
  map: { [key: string]: string } = {};
  string: [] = [];
  token: any;
  httpClient: HttpClient;
  isDarkThemeSubscription: boolean = false;
  isFiltering: boolean=false;
  filterKey: string= ''

  constructor(
    private themeService: ThemeServiceService,
    public dialog: MatDialog,
    private toastr: ToastrService,
    @Inject(BillInfoService) _service: BillInfoService
  ) {
    this.checkTheme();
    this.token = localStorage.getItem('accessToken');
    _service.defaultHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ` + this.token,
    });
    this._service = _service;
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

  ngOnInit(): void {
    this.checkTheme();
    this.getPagingApi(this.pageIndex, this.pageSize);
    this.getAllApi();
  }

  getPagingApi(pageIndex: number, pageSize: number) {
    this._service
      .apiBillInfoPagingGet(pageIndex, pageSize)
      .subscribe((result) => {
        this.listItems = result;
      });
  }

  getAllApi() {
    this._service.apiBillInfoPagingGet(0, 10).subscribe((result) => {
      this.pageDataTotalCount = Object.keys(result).length;
    });
  }

  /** [--IsDisableUpdate--]
  onClickEdit(id: any) {
    this.nameActionTrigger.emit({ type: 'edit', idItem: id });
  }
  [--IsDisableUpdate--] */

  reGetPagingData() {
    this.getPagingApi(this.pageIndex, this.pageSize);
  }

  gotoPrevious() {
    var sizePrevious = 0;
    sizePrevious = this.pageSize - 10;
    if (sizePrevious > 0) {
      this.pageSize = sizePrevious;
      this.getPagingApi(this.pageIndex, this.pageSize);
    }
  }

  gotoNext() {
    var sizeNext = 0;
    sizeNext =+ this.pageSize + +10;
    if (sizeNext > 0) {
      this.pageSize = sizeNext;
      this.getPagingApi(this.pageIndex, this.pageSize);
    }
  }

  /** [--IsDisableDelete--]
  onClickDelete(id: any) {
    const dialogRef = this.dialog.open(BillInfoDeleteUIComponent, {
      data: { idSelected: id },
    });
    dialogRef.afterClosed().subscribe((result) => {
      if (result.data) {
        this._service.apiBillInfoDelete(id).subscribe(
          (res) => {
            this.toastr.success("Delete successfully", "Notification");
            this.getPagingApi(this.pageIndex, this.pageSize);
            this.getAllApi();
          },
          (err) => {
            if (err.status === 400) {
              this.toastr.warning(err.error, 'Warning');
            }
          }
        );
      }
    });
  }
  [--IsDisableDelete--] */

  onClickView(id: any) {
    this.nameActionTrigger.emit({ type: 'read', idItem: id });
  }

  async applyFilter(event: any) {
    if (this.filterKey === '' ) {
      this.ngOnInit();
    } else if (event.code === 'Backspace') {
      this.ngOnInit();
      this.listItems = this.listItems.filter(item => {
        return ("" + item.id).trim().toLocaleLowerCase().includes(this.filterKey.toLocaleLowerCase());
      })
    } else{
      this.listItems = this.listItems.filter(item => {
        return ("" + item.id).trim().toLocaleLowerCase().includes(this.filterKey.toLocaleLowerCase());
      })
   }
  }
}

export interface DialogData {
  idSelected: any;
}
