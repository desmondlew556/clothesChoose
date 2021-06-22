import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import { Button } from './Button.js';
import './Carousel.css';

const men_clothes_base_url = '../../static/images/apparel/men/';
const women_clothes_base_url = '../../static/images/apparel/women/';
const base_url = '../static/images/others/';
const pic = require('./clothes.png');
const link = '../static/images/others/clothes.png';
class Carousel extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            image_descriptions: ['live music exploding in an outdoor concert',
            'elegant models walking down the carpet during a fashion show',
            'elegant models walking down the carpet during a fashion show'],
            image_url_array: ['concert.jpeg','fashion_show.jpg','fashion_show2.jpg'],
            current_image_index: 0,
            isChangeImage: false,
        }
    }
    change_image(index) {
        this.setState({
            isChangeImage: true
        })
        console.log(this.state.isChangeImage);
        this.setState({
            isChangeImage: false,
            current_image_index: index,
        })
        console.log(this.state.isChangeImage);
    }
    componentDidMount() {
        this.interval = setInterval(() => this.change_image((this.state.current_image_index + 1)%3),3000)
    }
    componentWillUnmount() {
        clearInterval(this.interval);
    }
    change_image_index(index) {
        this.change_image(index)
        clearInterval(this.interval);
        this.interval = setInterval(() => this.change_image((this.state.current_image_index + 1)%3),3000)
    }
    render() {
        return (
            <div className = "carousel-container">
                <img src = {require('../static/images/others/'+this.state.image_url_array[this.state.current_image_index])}
                alt = {this.state.image_descriptions[this.state.current_image_index]}
                className = {this.state.isChangeImage?'hero-image transition':'hero-image'} id = 'hero-img'/>
                
                <h1> Decide which clothes is better </h1>
                <p> What are you waiting for?</p>
                <div className = "hero-btns">
                    <Button
                        hasNextLink = {true}
                        nextLink = {this.props.link1}
                        buttonStyle = 'btn--primary' 
                    >
                        Get Started
                    </Button>
                    <Button
                        hasNextLink = {true}
                        nextLink = {this.props.link2}
                        buttonStyle = 'btn--outline' 
                    >
                        See Leaderboard
                    </Button>
                </div>
                <div className = "slider">
                    <Button
                        hasNextLink = {false}
                        onClick = {() => this.change_image_index(0)}
                        buttonStyle = 'btn--rounded'
                        buttonSize = 'btn--freesize'
                    >
                    </Button>
                    <Button
                        hasNextLink = {false}
                        onClick = {() => this.change_image_index(1)}
                        buttonStyle = 'btn--rounded'
                        buttonSize = 'btn--freesize'
                    >
                    </Button>
                    <Button
                        hasNextLink = {false}
                        onClick = {() => this.change_image_index(2)}
                        buttonStyle = 'btn--rounded'
                        buttonSize = 'btn--freesize'
                    >
                    </Button>
                </div>
            </div>
            
        )
    }
}
export default Carousel;