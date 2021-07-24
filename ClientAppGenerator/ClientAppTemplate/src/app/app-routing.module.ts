import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginScreenComponent } from './components/login-screen/login-screen.component';
import { NotFoundComponent } from './components/commons/not-found/not-found.component';
import { IndexUIComponent } from './components/user-logged-in/index-ui.component';
import { UserInformationComponent } from './components/user-logged-in/user-information/user-information.component';
import { LoginContentComponent } from './components/login-screen/login-content/login-content.component';
import { RegisterContentComponent } from './components/login-screen/register-content/register-content.component';
import { FooterComponent } from './components/user-logged-in/footer/footer.component';
/** ImportHere. */
import { AccountUpdateUIComponent } from './components/user-logged-in/account-table-ui/account-table-ui-action/account-update-ui-component/account-update-ui.component';
import { BillUpdateUIComponent } from './components/user-logged-in/bill-table-ui/bill-table-ui-action/bill-update-ui-component/bill-update-ui.component';
import { BillInfoUpdateUIComponent } from './components/user-logged-in/billinfo-table-ui/billinfo-table-ui-action/billinfo-update-ui-component/billinfo-update-ui.component';
import { FoodUpdateUIComponent } from './components/user-logged-in/food-table-ui/food-table-ui-action/food-update-ui-component/food-update-ui.component';
import { SystemLogUpdateUIComponent } from './components/user-logged-in/systemlog-table-ui/systemlog-table-ui-action/systemlog-update-ui-component/systemlog-update-ui.component';
import { TableFoodUpdateUIComponent } from './components/user-logged-in/tablefood-table-ui/tablefood-table-ui-action/tablefood-update-ui-component/tablefood-update-ui.component';
import { AccountcreateUIComponent } from './components/user-logged-in/account-table-ui/account-table-ui-action/account-create-ui-component/account-create-ui.component';
import { BillcreateUIComponent } from './components/user-logged-in/bill-table-ui/bill-table-ui-action/bill-create-ui-component/bill-create-ui.component';
import { BillInfocreateUIComponent } from './components/user-logged-in/billinfo-table-ui/billinfo-table-ui-action/billinfo-create-ui-component/billinfo-create-ui.component';
import { FoodcreateUIComponent } from './components/user-logged-in/food-table-ui/food-table-ui-action/food-create-ui-component/food-create-ui.component';
import { SystemLogcreateUIComponent } from './components/user-logged-in/systemlog-table-ui/systemlog-table-ui-action/systemlog-create-ui-component/systemlog-create-ui.component';
import { TableFoodcreateUIComponent } from './components/user-logged-in/tablefood-table-ui/tablefood-table-ui-action/tablefood-create-ui-component/tablefood-create-ui.component';
import { AccountReadUIComponent } from './components/user-logged-in/account-table-ui/account-table-ui-action/account-read-ui-component/account-read-ui.component';
import { BillReadUIComponent } from './components/user-logged-in/bill-table-ui/bill-table-ui-action/bill-read-ui-component/bill-read-ui.component';
import { BillInfoReadUIComponent } from './components/user-logged-in/billinfo-table-ui/billinfo-table-ui-action/billinfo-read-ui-component/billinfo-read-ui.component';
import { FoodReadUIComponent } from './components/user-logged-in/food-table-ui/food-table-ui-action/food-read-ui-component/food-read-ui.component';
import { SystemLogReadUIComponent } from './components/user-logged-in/systemlog-table-ui/systemlog-table-ui-action/systemlog-read-ui-component/systemlog-read-ui.component';
import { TableFoodReadUIComponent } from './components/user-logged-in/tablefood-table-ui/tablefood-table-ui-action/tablefood-read-ui-component/tablefood-read-ui.component';
import { AccountTableUIComponent } from './components/user-logged-in/account-table-ui/account-table-ui.component';
import { BillTableUIComponent } from './components/user-logged-in/bill-table-ui/bill-table-ui.component';
import { BillInfoTableUIComponent } from './components/user-logged-in/billinfo-table-ui/billinfo-table-ui.component';
import { FoodTableUIComponent } from './components/user-logged-in/food-table-ui/food-table-ui.component';
import { SystemLogTableUIComponent } from './components/user-logged-in/systemlog-table-ui/systemlog-table-ui.component';
import { TableFoodTableUIComponent } from './components/user-logged-in/tablefood-table-ui/tablefood-table-ui.component';

const routes: Routes = [
  { path: '', component: LoginContentComponent },
  { path: 'login', component: LoginContentComponent },
  { path: 'register', component: RegisterContentComponent },
  {
    path: 'user',
    component: IndexUIComponent,
    children: [
      { path: '', component: TableFoodTableUIComponent },

      { path: 'information', component: UserInformationComponent },
/** PathDeclareHere. */
      { path: 'index/accountmanagement/update/:id', component: AccountUpdateUIComponent },
      { path: 'index/billmanagement/update/:id', component: BillUpdateUIComponent },
      { path: 'index/billinfomanagement/update/:id', component: BillInfoUpdateUIComponent },
      { path: 'index/foodmanagement/update/:id', component: FoodUpdateUIComponent },
      { path: 'index/systemlogmanagement/update/:id', component: SystemLogUpdateUIComponent },
      { path: 'index/tablefoodmanagement/update/:id', component: TableFoodUpdateUIComponent },
      { path: 'index/accountmanagement/create', component: AccountcreateUIComponent },
      { path: 'index/billmanagement/create', component: BillcreateUIComponent },
      { path: 'index/billinfomanagement/create', component: BillInfocreateUIComponent },
      { path: 'index/foodmanagement/create', component: FoodcreateUIComponent },
      { path: 'index/systemlogmanagement/create', component: SystemLogcreateUIComponent },
      { path: 'index/tablefoodmanagement/create', component: TableFoodcreateUIComponent },
      { path: 'index/accountmanagement/view/:id', component: AccountReadUIComponent },
      { path: 'index/billmanagement/view/:id', component: BillReadUIComponent },
      { path: 'index/billinfomanagement/view/:id', component: BillInfoReadUIComponent },
      { path: 'index/foodmanagement/view/:id', component: FoodReadUIComponent },
      { path: 'index/systemlogmanagement/view/:id', component: SystemLogReadUIComponent },
      { path: 'index/tablefoodmanagement/view/:id', component: TableFoodReadUIComponent },
      { path: 'index/accountmanagement', component: AccountTableUIComponent },
      { path: 'index/billmanagement', component: BillTableUIComponent },
      { path: 'index/billinfomanagement', component: BillInfoTableUIComponent },
      { path: 'index/foodmanagement', component: FoodTableUIComponent },
      { path: 'index/systemlogmanagement', component: SystemLogTableUIComponent },
      { path: 'index/tablefoodmanagement', component: TableFoodTableUIComponent },
    ],
  },
  { path: 'footer', component: FooterComponent },
  { path: '**', component: NotFoundComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
