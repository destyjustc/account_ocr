import { Component, AfterViewInit, ApplicationRef} from '@angular/core';
// import { FileUploader } from 'ng2-file-upload';
import {UPLOAD_DIRECTIVES} from 'ng2-file-uploader/ng2-file-uploader';
import { ApiService } from './shared';

declare var $;

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent implements AfterViewInit{
    // public uploader:FileUploader = new FileUploader({url: URL});
    // public hasBaseDropZoneOver:boolean = false;
    fileId:string;
    filePath = '';
    postId: number;
    BASE_URL = '';
    options: Object;
    cropImg = [];
    uploaded_files = [];
    file_index = 0;
    file_count = 0;

    zoom = 1;
    downloadLink = '';

    collection = [];
    jcrop_api: any;

    constructor(
        private apiService: ApiService,
        private applicationRef: ApplicationRef
    ) {
        this.BASE_URL = apiService.getBaseUrl();
        this.options = {
            url: this.BASE_URL+'/upload',
            params: { 'post_id': this.postId }
        };
    }

    handleUpload(data): void {
        if (data && data.response) {
            data = JSON.parse(data.response);
            data = JSON.parse(data)
            this.uploaded_files = data;
            this.file_count = data.length;
            this.fileId = data[0].id
            this.filePath = this.BASE_URL+'/file/'+data[0].filename;
            this.collection = data;
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
            vm.apiService.mwPostJson('/coors/'+vm.fileId, obj).subscribe((data) => {
                console.log(data);
                data = JSON.parse(data)
                let obj = {
                    img: vm.BASE_URL+'/file/'+data.filename,
                    positions: data.locations,
                    results: data.results,
                    id: data.id
                };
                vm.cropImg.push(obj);
                console.log(vm.cropImg);
                vm.applicationRef.tick();
            });
        }
    }

    activateAreaSelection() {
        let vm = this;
        $('#input-image').Jcrop({
            onSelect: this.sendCoors(),
            boxWidth: 1600,   //Maximum width you want for your bigger images
            boxHeight: 800,  //Maximum Height for your bigger images
        }, function() {
            vm.jcrop_api = this;
        });
    }

    getResultItemStyle(p) {
        return {
            'position': 'absolute',
            'top': p[0]+'px',
            'line-height': (p[1]-p[0])*this.zoom+'px',
            'left':'0px',
            'min-width': '172px'
        };
    }

    onSubmit() {
        let vm = this;
        vm.apiService.mwPutJson('/coors/'+vm.fileId, this.cropImg).subscribe((data) => {
            vm.apiService.mwGet('/csv/'+this.fileId).subscribe((res) => {
                res = JSON.parse(res);
                this.downloadLink = this.BASE_URL+'/file/'+res;
                window.location.assign(this.downloadLink);
            });
        });
    }

    onPageChange(event) {
        this.cropImg = [];
        this.file_index = event - 1;
        this.fileId = this.uploaded_files[this.file_index].id
        this.filePath = this.BASE_URL+'/file/'+this.uploaded_files[this.file_index].filename;
        // $('.jcrop-holder img').attr('src', this.filePath);
        this.jcrop_api.setImage(this.filePath);
        // this.jcrop_api.setImage(this.filePath);
        // console.log(this.filePath);
    }
}
