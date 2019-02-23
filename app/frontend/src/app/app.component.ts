import { Component, OnInit } from '@angular/core';
import { DataApiService } from './data-api.service';
import { Subscription } from 'rxjs/Subscription';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {

  title = 'CelsiusPro Coding Test';
  selStation = ''
  selVariable = ''
  variablesNames = []
  stationsIds = []

  constructor(private dataApi: DataApiService) {
  }

  refreshIds() {
    this.dataApi
      .getIds()
      .subscribe(data => {
          this.variablesNames = data['varsNames'];
          this.stationsIds = data['stationsIds'];
        },
        console.error
      );
  }

  ngOnInit() {
    this.refreshIds();
  }

  plotSeries() {
    if (this.selStation !== '' && this.selVariable !== '') {
      this.dataApi.getData(this.selStation, this.selVariable)
        .subscribe(data => {
          console.log(data['records']);
        },
        console.error
      );;
    }   
  }

  downloadFiles() {
    this.dataApi.downloadFiles()
      .subscribe(data => {
        console.log(data['numFiles'] + ' files downloaded');
        this.refreshIds();
      },
      console.error
    );;  
  }
}
