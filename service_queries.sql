SELECT entretaiment.entertainment_id, entretaiment.entertainment_name, COUNT(preferred_content_id) AS people FROM entretaiment, users WHERE preferred_content_id = entretaiment.entertainment_id GROUP BY entretaiment.entertainment_id;
//Muestra el tipo de entretenimiento que prefiere la gente

