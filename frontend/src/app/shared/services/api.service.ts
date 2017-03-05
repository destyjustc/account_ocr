import { Injectable } from '@angular/core';
import { Http, Headers } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import { environment } from '../../../environments/environment';


@Injectable()
export class ApiService {
    static defaultHeader: Headers;
    static mwBaseUrl: string = '/api';
    static init: boolean = false;

    constructor(
        private http: Http
        ) {
    	if (!ApiService.init) {
            ApiService.defaultHeader = new Headers();
            ApiService.defaultHeader.append('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        }
        if (!environment.production) {
            this.setBaseUrl('http://127.0.0.1:5000/api');
        }
        // let _build = (<any> http)._backend._browserXHR.build;
        // (<any> http)._backend._browserXHR.build = () => {
        //     let _xhr = _build();
        //     _xhr.withCredentials = true;
        //     return _xhr;
        // };
    }

    getBaseUrl() {
        return ApiService.mwBaseUrl;
    }

    setBaseUrl(url: string) {
        ApiService.mwBaseUrl = url;
    }

    // get mw API
    mwGet(url: string, header?: Headers) {
        let vm = this;
        let h = header ? header : ApiService.defaultHeader;
        return this.http.get(ApiService.mwBaseUrl + url, {headers: h}).map(res => res.json()).catch(vm.handleError());
    }

    mwPutJson(url: string, param?: any, header?: Headers) {
        let vm = this;
        let h = header ? header : new Headers({ 'Content-Type': 'application/json' });
        return this.http.put(ApiService.mwBaseUrl + url, param, {headers: h}).map(res => res.json()).catch(vm.handleError());
    }

    mwPost(url: string, param?: any, header?: Headers) {
        let vm = this;
        let h = header ? header : ApiService.defaultHeader;
        return this.http.post(ApiService.mwBaseUrl + url, param, {headers: h}).map(res => res.json()).catch(vm.handleError());
    }

    mwPostJson(url: string, param?: any) {
        let vm = this;
        let h = new Headers({ 'Content-Type': 'application/json' });
        return this.http.post(ApiService.mwBaseUrl + url, param, {headers: h}).map(res => res.json()).catch(vm.handleError());
    }

    mwDelete(url: string, header?: Headers) {
        let vm = this;
        let h = header ? header : ApiService.defaultHeader;
        return this.http.delete(ApiService.mwBaseUrl + url, {headers: h}).map(res => res.json()).catch(vm.handleError());
    }

    get(url: string, params?: any[]): any {
        let vm = this, paramString = '';
        if (params && params.length > 0) {
            paramString = '?' + params.join('&');
            paramString = paramString.replace(/\s/g, '');
        }
        return this.http.get(url + paramString).map(res => res.json()).catch(vm.handleError());
    }

    private handleError() {
        return (error: any) => {
        	return Observable.throw(error);
        };
    }
}
