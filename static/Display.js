// This file defines a Display object, which is the main part of the
// client program.  It controls the content and position of the
// canvases.
//

function Display() {

    var me = this; // convention for local use of self

    // Set listeners and associated event handlers.
    this.initListeners = function () { // --------------------------------------- initListeners

        $( '#reset-crosshairs' ).click( function ( e ) {
	   var  // local declarations
	      canvas = $( "#axis" )[0],
	      context = canvas.getContext( "2d" );

	    me.crosshairX = 1;
	    me.crosshairY = 0;

	    me.clearCanvas( "#axis" );

	    // display the position with text above the plot
	    $( '#crosshair-position' ).html( "Column " + (me.crosshairX) + ", Row " + (me.crosshairY));
	    me.updateNeighboringPlots( me.crosshairX, me.crosshairY );
	});

	$( '#high-level-view' ).click(function (e) {
	    //		window.location.href = '#spectrum-0';
	});

        // Registering click event for the plot.
        // On click, get the position of the click and draw cross
        // hairs to highlight the row and column clicked.  Then update
        // the timeseries and spectral plots to show the selected row
        // and column (channel).
        $( '#axis' ).click(function (e) {
           var // local declarations
	      canvas = $( "#axis" )[0],
	      context = canvas.getContext( "2d" );

            // get click pos relative to left edge of plot
            // http://api.jquery.com/event.pageX/
            me.crosshairX = Math.floor( e.pageX - $( "#axis" ).offset().left );

            // get click pos relative to top of plot
            // http://api.jquery.com/event.pageY/
            me.crosshairY = Math.floor( e.pageY - $( "#axis" ).offset().top );

            me.clearCanvas( "#axis" );

            // draw crosshairs
            context.beginPath();
            context.moveTo( me.crosshairX - 1, 0 );
            context.lineTo( me.crosshairX - 1, me.canvasHeight );
            context.moveTo( 0, me.crosshairY - 1 );
            context.lineTo( me.canvasWidth, me.crosshairY - 1 );
            context.strokeStyle = 'yellow'; // make the crosshairs red
            context.stroke();

            // display the position with text above the plot
            $( '#crosshair-position' ).html( "Column " + ( me.crosshairX ) + ", Row " + ( me.crosshairY ) );
            me.updateNeighboringPlots( me.crosshairX, me.crosshairY );
	    });

        $( '#bank-choice' ).change(function () {
            // stop requesting data
            clearTimeout(me.updateId);

	    // clear neighboring plots
            me.drawSpecUnderWaterfall(null);
            me.drawTimeSeries(null);

            // clear the plot display
            me.resetDisplay();

            me.currentBank = $( '#bank-choice').find( ':checked').val();
            console.log("----------------- Changed to bank " + me.currentBank);

	    // hide subband buttons
	    $( '#subband-choice > input').prop("disabled", true);

            // request data every 1 second for new bank
            me.startRequestingData();
        });

        $( '#subband-choice' ).change(function () {
            // stop requesting data
            clearTimeout( me.updateId );

	    // clear neighboring plots
            me.drawSpecUnderWaterfall( null );
            me.drawTimeSeries( null );

            // clear the plot display
            me.resetDisplay();

            me.currentSubband = $( '#subband-choice' ).find( ':checked' ).val();
            console.log( "----------------- Changed to subband " + me.currentSubband );

            // request data every 1 second for new bank
            me.startRequestingData();
        });

    }; // +++++++++++++++++++++++++++ end of initListeners

    this.clearCanvas = function ( id ) { // --------------------------------------- clearCanvas
        var canvas = $( id )[0];
        canvas.width = canvas.width;
        canvas.height = canvas.height;
    };

    // when we want to switch to displaying a different bank we
    // need to clear the plot and axes
    this.resetDisplay = function () { // --------------------------------------- resetDisplay

        // clear each of the two plot canvases
        this.clearCanvas( this.primaryCanvas );
        this.clearCanvas( this.secondaryCanvas );

        // reset the canvas top positions
        $( this.primaryCanvas ).css( "top", "-350px" );
        $( this.secondaryCanvas ).css( "top", "150px" );

	this.rowCounter = 0;
    };

    this.updateNeighboringPlots = function ( x, y ) { // --------------------------------------- updateNeighboringPlots

        // Convert the (x, y) position for the mouse click to the right indices.
        this.channel_index = Math.floor(  x / this.pointWidth );
        this.spectrum_index = Math.floor( y / this.pointHeight );

        console.log( " x " + x + 
		     " pointWidth " + this.pointWidth + 
		     " y " + y + 
		     " pointHeight " + this.pointHeight );
        console.log( "clicked spectrum at: " + 
		     "[row " + this.spectrum_index + "," +
		     " channel " + this.channel_index + "]" );

        // If we clicked where there is data plot, tell the spectra plot to display that
        // row.  Otherwise, we clear the spectrum plot.
        if ( this.spectrum_index < this.waterfallSpectra.length &&
	     this.spectrum_index >= 0 ) {

            var spectrum = this.waterfallSpectra[this.spectrum_index];
            this.drawSpecUnderWaterfall( spectrum );

        } else {

            this.drawSpecUnderWaterfall( null );
        }

        if ( this.channel_index < this.waterfallSpectra[0].length &&
	     this.channel_index >= 0 ) {

	    // create a time series array, initialized to null
           var timeSeries = new Array( this.nSpectra );
            for (var i = 0; i < timeSeries.length; i++ ) { timeSeries[i] = null; }

	    // set values only for the number of spectra displayed in selected channel
	    for (var jj = 0; jj < this.rowCounter; jj++ ) {
                timeSeries[jj] = this.waterfallSpectra[jj][this.channel_index];
            }
            console.log( 'updating time series, length', timeSeries.length );
            this.drawTimeSeries( timeSeries );
        } else {
            this.drawTimeSeries( null );
        }

    };

    this.getMin = function (data) {
        Array.prototype.min = function () {
            return Math.min.apply(null, this);
        };
        return Math.min.apply(null, data);
    };

    this.getMax = function (data) {
        Array.prototype.max = function () {
            return Math.max.apply(null, this);
        };
        return Math.max.apply(null, data);
    };

    this.addData = function (data) { // --------------------------------------- addData

        // If we have reached the max amount of data to keep in
        // the buffer, pop off the end.
        if (this.waterfallSpectra.length >= this.nSpectra) {
            this.waterfallSpectra.pop();
        }

        // If we have plotted the max amount of data, swap the
        // canvases and reset the count.
        if (this.rowCounter >= this.nSpectra) {
            console.log("= " + this.rowCounter + " " + this.nSpectra);

            // Also, if we've been plotting on the second cavnas,
            // clear the secondary before the swap.
            $(this.secondaryCanvas).css("top", "-350px");
            this.clearCanvas(this.secondaryCanvas);
           var temp = this.primaryCanvas;
            this.primaryCanvas = this.secondaryCanvas;
            this.secondaryCanvas = temp;
            this.rowCounter = 0;
        } else {
            console.log( 'used ' + this.rowCounter +
			" of " + this.nSpectra + " available rows in plot");
        }

        // Finally, insert the new data to the beginning of the
        // buffer.
        this.waterfallSpectra.unshift(data);
    };

    this.drawTimeSeries = function (data) { // --------------------------------------- drawTimeSeries
        $("#timeseries").highcharts({
            chart: { animation: false },
            legend: { enabled: false },
            credits: { enabled: false },
            title: { text: 'Time Series' },
            series: [{
                name: 'amplitude',
                linewidth: 1,
                marker: { enabled: false },
                animation: false,
                data: data,
            }],
            tooltip: { enabled: false },
            plotOptions: {
		    series: {
			states: {
			    hover: { enabled: false }
			}, 
			lineWidth: 1
		    }
	    },
            yAxis: {
		    type: 'logarithmic',
		    title: { text: null },
		    labels: {
			formatter: function () {
			    return this.value.toPrecision(2);
			}
		    }
	    },
	});
    };

    this.drawSpecUnderWaterfall = function(data) { // --------------------------------------- drawSpecUnderWaterfall
        $("#waterfall-spectrum").highcharts(me.waterfallSpecOptions);

	var wfspec = $( '#waterfall-spectrum').highcharts();
	wfspec.series[0].setData(data);
	wfspec.setTitle({text: 'Spectrum'});
    };

    this.drawSpec = function(number, bank, data) {
	// maybe use arguments feature of js instead of dataA, dataB, etc.
	// and a for loop for setData to iterate over arguments
        $("#spectrum-" + number).highcharts(me.specoptions);
	var specchart = $( '#spectrum-'+number).highcharts();
	data[bank].forEach( function(subband, index, array) {
	    specchart.series[index].setData(subband);
	});
	specchart.setTitle({text: 'Spectrometer '+bank});
    };

    this.startRequestingData = function () { // --------------------------------------- startRequestingData
       var me = this; // convention for local use of self
        me.updateId = setInterval(function () {
            me.ws.send( 'data');
        }, 3*1000); // 1000 milliseconds == 1 second
	console.log( 'update id: ' + me.updateId); // debug
    };

    this.drawDisplay = function (data) {  // --------------------------------------- drawDisplay
        // First a few words about how the waterfall plot is done.
        // In order to avoid redrawing every rectangle each time
        // we get a new sample, I'm stacking each sample on top of
        // the previous ones and moving the canvas down.  That way
        // we only plot the latest sample (row).  We keep track of
        // how many rows we have plotted and use it to find the
        // new position for the canvas.  Now, there are actually 3
        // total canvases we draw on.  One for the axis and two
        // for the waterfall.  There are two for the waterfall so
        // we can continuiously plot the data.  When the primary
        // canvas fills up, we swap it with the secondary one.
       var
	  canvas = $(this.primaryCanvas)[0];
          canvas2 = $(this.secondaryCanvas)[0];
          context = canvas.getContext("2d");
          context2 = canvas2.getContext("2d");

        // Given the number of rows we have plotted, what should the position be?
        this.rowCounter += 1;

        // Set the canvases top position accordingly.
        $(this.primaryCanvas).css("top", $(this.primaryCanvas).position().top + this.pointHeight);
        $(this.secondaryCanvas).css("top", $(this.secondaryCanvas).position().top + this.pointHeight);
        console.log("height " + this.pointHeight);
        console.log("canvas 1 top " + $(this.primaryCanvas).position().top);
        console.log("canvas 2 top " + $(this.secondaryCanvas).position().top);

        // Draw the new spectrum as rectangles
        for (var chan = 0; chan < data.length; chan++) {
            context.fillStyle = this.getFillColor(Math.log(data[chan]));
            context.fillRect(this.pointWidth * chan,
            this.canvasHeight - (this.pointHeight * this.rowCounter),
            this.pointWidth, this.pointHeight);
        }

        // Clip the bottom of the secondary canvas
       var clipPos = Math.round(canvas2.height - (this.pointHeight * this.rowCounter));
        context2.clearRect(0, clipPos, this.canvasWidth, (this.pointHeight * this.rowCounter));
    };

    this.getFillColor = function (value) { // --------------------------------------- getFillColor

       var colorIdx = Math.floor(((value - this.colormin) / (this.colormax - this.colormin)) * 255);
        return 'rgb(' + colorIdx + ',0,0)';
    };

    // set waterfall lower spectrum plot position and width
    $("#waterfall-spectrum").css("top", $("#axis").position().top + $("#axis").height());
    $("#waterfall-spectrum").css("width", $("#axis").width());

    this.canvasWidth = $("#axis").width(); // canvas width, in pixels
    this.canvasHeight = $("#axis").height(); // canvas height, in pixels

    // make the bank radio button choices a jquery-ui buttonset
    $("#bank-choice").buttonset();
    $( '#bank-choice > label').first().click()
    $( '#subband-choice > input').prop("disabled", true);
    $("#subband-choice").buttonset();
    this.currentBank = null;

    this.nSpectra = 100; // number of spectra in waterfall plot
    this.waterfallSpectra = new Array(this.nSpectra);


    // datapoint height and width, in pixels
    this.pointHeight = this.canvasHeight / this.nSpectra;
    this.pointWidth = undefined; // calculated later

    // offsets from left and top of window; needed to translate
    // click events to positions on the waterfall plot
    this.horzOffset = 0;
    this.vertOffset = 0;

    this.rowCounter = 0; // keeps track of the current row position

    // waterfall index of time series to display in the spectrum plot
    this.channel_index = 1;

    // waterfall index of spectrum to display in the spectrum plot
    this.spectrum_index = 0;

    // these will switch as each canvas slides below the viewable area
    this.primaryCanvas = "#waterfallA";
    this.secondaryCanvas = "#waterfallB";
    this.colormax = null; // for color normalization
    this.colormin = null; // for color normalization

    this.updateId = null; // used to control update interval

    // position of the crosshairs
    // this determines what is displayed in the neighboring
    // time series and spectrum plots
    this.crosshairX = 1; // default to channel 0
    this.crosshairY = 0; // default to most recent spectrum

    // highcharts display options object
    this.specoptions =  {
        chart: { animation: false },
	legend: { title: 'Subband', layout: 'vertical', verticalAlign: 'top', align: 'right' },
        credits: { enabled: false },
        series: [{name: '0', marker: { enabled: false }, animation: false },
                 {name: '1', marker: { enabled: false }, animation: false },
                 {name: '2', marker: { enabled: false }, animation: false },
                 {name: '3', marker: { enabled: false }, animation: false },
                 {name: '4', marker: { enabled: false }, animation: false },
                 {name: '5', marker: { enabled: false }, animation: false },
                 {name: '6', marker: { enabled: false }, animation: false },
                 {name: '7', marker: { enabled: false }, animation: false }],
        tooltip: { enabled: false },
        plotOptions: {
            series: {
                states: { hover: { enabled: false } },
		lineWidth: 2
            }
        },
        yAxis: {
            type: 'logarithmic',
            title: { text: "counts" },
	    labels: {
		formatter: function () {
		    return this.value.toPrecision(2);
		}
	    }
        },
        xAxis: {
            title: { text: "GHz" },
	    labels: {
		formatter: function () {
		    return this.value/1e9
		}
	    }
        },
    };

    // highcharts display options object
    this.waterfallSpecOptions =  {
        chart: { animation: false },
	legend: { enabled: false },
        credits: { enabled: false },
	series: [{
                name: 'amplitude',
                linewidth: 1,
                marker: { enabled: false },
                animation: false,
            }],
        tooltip: { enabled: false },
        plotOptions: {
            series: {
                states: { hover: { enabled: false } },
		lineWidth: 2
            }
        },
        yAxis: {
            type: 'logarithmic',
            title: { text: null },
	    labels: {
		formatter: function () {
		    return this.value.toPrecision(2);
		}
	    }
        },
    };

    // initialize event listeners
    this.initListeners();

    // initialize subband to 0
    this.currentSubband = 0;

};  // +++++++++++++++++++++++++++++++++++++++++  end of Display function


function amplitudes(ampAndSkyFreq) {  // --------------------------------------- amplitudes
    // create a 1d array of the same length as the first dim of the 2d array
   var amps = new Array(ampAndSkyFreq.length);
    // put all the first index elements of the 2d array in the 1d array
    for (var i = 0; i < ampAndSkyFreq.length; i++) {
	amps[i] = ampAndSkyFreq[i][1];
    }
    return amps;
}

// ------------------------------------- methods defined above

// instantiate a Display object
var realtimeDisplay = new Display();

// Open the web socket to the data source, which is the tornado server that
// that is reading from the streaming manager(s)
var hostname = $("#hostname").html();
var port = $("#port").html();
realtimeDisplay.ws = new WebSocket("ws://" + hostname + ":" + port + "/websocket");

realtimeDisplay.ws.onopen = function (event) {
    realtimeDisplay.ws.send( 'active_banks'); // request a list of active banks
};

realtimeDisplay.ws.onclose = function (event) {
    clearTimeout(me.updateId);
    console.log( 'web socket closed');
    $( '#status').html( 'No display connection.  Try refresh.');
    $( '#status').css( 'color', 'red');
};

realtimeDisplay.ws.onerror = function (event) {
    clearTimeout(me.updateId);
    console.log( 'web socket error');
    $( '#status').html( 'Unknown error.  Try refresh.');
    $( '#status').css( 'color', 'red');
};

// Handle data sent from the write_message server code in vdd_stream_socket.py
var me = realtimeDisplay;

try {
realtimeDisplay.ws.onmessage = function (evt) {
   var msg = JSON.parse(evt.data);
    console.log(msg.header)

    if ( 'bank_config' === msg.header) {
	// set the radio button properties depending on what banks
	// are available
	var bank_arr = msg.body;
	$.each(bank_arr, function (index, bank) {
                console.log( 'enabling bank', bank);
            });

	me.currentBank = bank_arr[0];
	$( '#header').html( 'Spec ' + me.currentBank + ', SB ' + me.currentSubband);

	// send msg to server with default bank to display
	// request data every 1 second
	me.startRequestingData();

    } else if ( 'data' === msg.header) {
	var 
	  Banknum = {'A':0, 'B':1, 'C':2, 'D':3,
		     'E':4, 'F':5, 'G':6, 'H':7},
	  md = msg.body.metadata,
	  spectra = msg.body.spectra;

	console.log('spectra',spectra);

	// display some metadata on screen
	$( '#header').html( 'Spec ' + me.currentBank + ', Band ' + me.currentSubband);
	$( '#metadata').html( 'Project id: ' + md.project + ', ' +
			    'Scan: ' + md.scan + ', ' +
			    'Int: ' + md.integration);
	// debug info
	console.log( 'bank', me.currentBank );
	console.log( 'project', md.project );
	console.log( 'scan', md.scan );
	console.log( 'state', md.state );
	console.log( 'update waterfall:', md.update_waterfall );
	console.log( 'length of data (number of subbands):', spectra[me.currentBank].length );

	// set the first and last channel of every spectrum to null
	// this avoids displaying a common huge spike in the first channel
 	for (var bank in spectra) {
	    console.log(spectra, bank, spectra[bank]);
	    if (spectra[bank].length > 0) {
		// for each subband on this bank
		spectra[bank].forEach(function(subband, index, array) {
		    var firstChan = 0;
		    var lastChan = subband.length - 1;
		    var amplitude = 1; // freq. element is 0 (freq, amplitude)
		    subband[firstChan][amplitude] = null;
		    subband[lastChan][amplitude] = null;
		});
	    }
	}
        
	// for each subband of the current bank
	spectra[me.currentBank].forEach(function(subband, index, array) {
	   var selector_string = '#subband-choice > input:eq(' + index + ')';
	    $(selector_string).prop("disabled", false);
	});

	$("#subband-choice").buttonset("refresh");
	$( '#subband-choice > label')[me.currentSubband].click();

	if (md.update_waterfall == 1)
	    {
		try {
		   var amps = amplitudes(spectra[me.currentBank][me.currentSubband]);
		}
		catch(err) {
		    console.log( 'ERROR');
		    console.log(spectra);
		}
		me.pointWidth = me.canvasWidth / amps.length;
		me.addData(amps);
		me.colormin = Math.log(me.getMin(amps.slice(1,-1))); // omit first and last channels
		me.colormax = Math.log(me.getMax(amps.slice(1,-1)));
		me.drawDisplay(amps);
		me.updateNeighboringPlots(me.crosshairX, me.crosshairY);
		$( '#status').html( 'Running');
		$( '#status').css( 'color', 'green');
	    }
	else
	    {
		$( '#status').html( 'Waiting for data');
		$( '#status').css( 'color', 'orange');
	    }
	
	// draw the spec plots for all banks and subbands
	for (var bank in Banknum) {
	    var banknum = Banknum[bank];
	    var select_string = "#bank-choice > label:eq(" + banknum + ") span";
	    var bankdata = spectra[bank];

	    if ( bankdata.length > 0 ) {
		$(select_string).css({color: "green"});
	    } else {
		$(select_string).css({color: "grey"});		
	    }
	    me.drawSpec((banknum).toString(), bank, spectra);
	}
    } else {
	console.log( 'Not updating for message:', msg.header);
    }
};
}
catch(err) {
    console.log('ERROR:', err.message);
}