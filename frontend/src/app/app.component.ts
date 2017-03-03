import { Component, AfterViewInit } from '@angular/core';
// import { FileUploader } from 'ng2-file-upload';
import {UPLOAD_DIRECTIVES} from 'ng2-file-uploader/ng2-file-uploader';
import { ApiService } from './shared';

declare var $;

const BASE_URL = '/api';
@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.css']
})
export class AppComponent implements AfterViewInit{
    // public uploader:FileUploader = new FileUploader({url: URL});
    // public hasBaseDropZoneOver:boolean = false;
    fileId:string;
    filePath = '';
    postId: number;
    options: Object = {
        url: BASE_URL+'/upload',
        params: { 'post_id': this.postId }
    };
    cropImg = []

    constructor(
        private apiService: ApiService
    ) {
        console.log(apiService);
    }

    handleUpload(data): void {
        if (data && data.response) {
            data = JSON.parse(data.response);
            data = JSON.parse(data)
            this.fileId = data.id
            this.filePath = BASE_URL+'/file/'+data.filename;
            setTimeout(() => {
                this.activateAreaSelection()
            }, 200);
        }
    }

    ngAfterViewInit() {
    }

    sendCoors() {
        let vm = this;
        return function(c){
            console.log(c)
            let obj = {
                top: c.y,
                bottom: c.y2,
                left: c.x,
                right: c.x2
            };
            vm.apiService.mwPostJson(BASE_URL+'/coors/'+vm.fileId, obj).subscribe((data) => {
                console.log(data);
                data = JSON.parse(data)
                vm.cropImg.push(BASE_URL+'/file/'+data.filename);
                console.log(vm.cropImg);
            });
        }
    }

    activateAreaSelection() {
        $('#input-image').Jcrop({
            onSelect: this.sendCoors()
        })
    }
}
