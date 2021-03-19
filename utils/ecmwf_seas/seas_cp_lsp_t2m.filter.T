# split cp,lsp,t2m variables for each seperate ensemble
# filename format seas.yyymmdd.en_xx.gbrib

if ( cfVarName is 'cp'  || cfVarName is 'lsp' || cfVarName is 't2m' ) {
	
	
	if (perturbationNumber < 10){ 
		write "{{out_dir}}/seas.[dataDate].en_0[perturbationNumber].grib"; 
	}
	else { 
		write "{{out_dir}}/seas.[dataDate].en_[perturbationNumber].grib"; 
	}
}
