(() => {
    // Localiza el iframe principal
    const mainFrame = document.getElementById("mainFrame");
    if (!mainFrame) {
      console.log("No existe un iframe con id='mainFrame' en el documento padre.");
      return;
    }
  
    // Accede al documento interno de mainFrame
    const mainDoc = mainFrame.contentDocument || mainFrame.contentWindow.document;
    if (!mainDoc) {
      console.log("No se pudo acceder al documento de mainFrame (probable cross-domain o no cargado aún).");
      return;
    }
  
    // Ahora, dentro de mainDoc, busca el iframe 'iFrameEncargos'
    const encargosFrame = mainDoc.getElementById("iFrameEncargos");
    if (!encargosFrame) {
      console.log("No se encontró un iframe con id='iFrameEncargos' dentro de mainFrame.");
      return;
    }
  
    // Accedemos al documento interno de iFrameEncargos
    const encargosDoc = encargosFrame.contentDocument || encargosFrame.contentWindow.document;
    if (!encargosDoc) {
      console.log("No se pudo acceder al documento interno de iFrameEncargos.");
      return;
    }
  
    // Aquí podrías ya hacer el query de los enlaces de descarga
    // Ejemplo: buscar y simular clic
    const links = encargosDoc.querySelectorAll('a[title="Descargar"]');
    if (links.length === 0) {
      console.log("No se encontraron enlaces con title='Descargar' dentro de iFrameEncargos.");
      return;
    }
  
    links.forEach(link => link.click());
    console.log(`Iniciada descarga de ${links.length} archivo(s).`);
  })();
  