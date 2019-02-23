import { Injectable } from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {API_URL} from '../env';

@Injectable({
  providedIn: 'root'
})
export class DataApiService {

  constructor(private http: HttpClient) { }

  getIds() {
    return this.http
      .get(`${API_URL}/get_ids`);
  }

  downloadFiles() {
    return this.http
      .get(`${API_URL}/download_files`);
  }

  getData(stationId, variableName) {
    return this.http
      .get(`${API_URL}/get_data/${stationId}/${variableName}`);  
  }
}
