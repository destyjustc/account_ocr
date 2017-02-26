import { UploadItem }    from 'angular2-http-file-upload';
 
export class MyUploadItem extends UploadItem {
    constructor(file: any) {
        super();
        this.url = 'http://localhost:5000/upload';
        this.file = file;
    }
}