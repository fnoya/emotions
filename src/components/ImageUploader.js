import React, { useState } from 'react';
import Dropzone from 'react-dropzone';
import axios from 'axios';
import './ImageUploader.css';

function ImageUploader() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);

  const handleFileSelect = (files) => {
    const selected = files[0];
    setSelectedFile(selected);
    const preview = URL.createObjectURL(selected);
    setPreviewImage(preview);
  };

  const handleFileUpload = async () => {
    console.log("handleFileUpload")
    const formData = new FormData();
    formData.append('image', selectedFile);
    try {
      const response = await axios.post('/detect_emotions', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        responseType: 'arraybuffer'
      });
      const blob = new Blob([response.data], { type: 'image/jpeg' });
      const preview = URL.createObjectURL(blob);
      setPreviewImage(preview);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <div>
        {previewImage ? (
          <img src={previewImage} alt="Preview" />
        ) : (
          <p className='text'>Selecciona una imagen</p>
        )}
      </div>
      <Dropzone onDrop={handleFileSelect} >
        {({ getRootProps, getInputProps }) => (
            <section className='image-uploader'>
                <div {...getRootProps()} >
                  <input {...getInputProps()} />
                  <p className='text'>Arrastra y suelta una imagen aquí o haz clic para seleccionar</p>
                </div>
              </section>
        )}
      </Dropzone>
      {selectedFile && (
        <button className='big-button' onClick={handleFileUpload}>Procesar imagen</button>
      )}
    </div>
  );
}

export default ImageUploader;
