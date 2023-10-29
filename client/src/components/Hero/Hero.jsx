const Hero = () => {

    return(
        <div className="container mt-5">
            <div className="row justify-content-center gx-5">
                <div className="col-12 col-xl-5">
                    <img src="https://www.w3schools.com/css/grid_lines.png" alt="image" style={{ width: '460px', height: '460px'}}/>
                </div>
                <div className="col-12 col-xl-7 p-5">
                    <h1>
                        Your trusted platform for buy and selling
                    </h1>
                    <p>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec facilisis quam. Vivamus interdum, turpis vel varius auctor, sapien elit fermentum metus, eget tincidunt dolor ex sit amet purus.
                    </p>
                    <button>
                        Shopping
                    </button>

                    <button>
                        Selling
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Hero;