import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DeleteUIComponent } from './delete-ui.component';

describe('DeleteUIComponent', () => {
  let component: DeleteUIComponent;
  let fixture: ComponentFixture<DeleteUIComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DeleteUIComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DeleteUIComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
