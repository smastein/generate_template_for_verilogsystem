module test # (
		CNT_MAX=100,
		CNT_WIDTH=8

		//USER PARAMETERS BEGIN
		jezeli tu cos wpisze
		//USER PARAMETERS END
	) (
		input logic clk_i,
		input logic rst_n_i,

		//USER PORTS BEGIN
		albo tu
		//USER PORTS END

		input logic a,
		input logic [31:0] vector,
		input logic [CNT_WIDTH-1:0] vect_in,

		output logic b,
		output logic [CNT_WIDTH-1:0] vect_out,

		inout logic scl,
		inout logic sda,

	};

	logic [3:0] sum;
	logic state;

	logic b_nxt;
	logic [CNT_WIDTH-1:0] vect_out_nxt;

	logic [3:0] sum_nxt;
	logic state_nxt;

	//USER VARIABLES BEGIN
	to nic z tego sie nie usunie
	//USER VARIABLES END

	always_comb begin
		b_nxt	= b;
		vect_out_nxt	= vect_out;

		sum_nxt	= 'h0;
		state_nxt	= state;
		//USER COMB BEGIN

		//USER COMB END
	end

	always_ff @(posedge clk_i or negedge rst_n_i) begin
		if(rst_n_i = 1'b0) begin
			b	<= 'h1;
			vect_out	<= 'h0;

			sum	<= 'h0;
			state	<= 'h0;

			//USER RESETS BEGIN

			//USER RESETS END
		end
		else begin
			b	<= 'h0;
			vect_out	<= 'h0;

			sum	<= sum_nxt;
			state	<= state_nxt;

			//USER CLOCK BEGIN

			//USER CLOCK END
		end
	end
endmodule;
