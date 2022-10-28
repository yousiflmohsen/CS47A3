import { StyleSheet, Image,SafeAreaView, Text,View,Pressable,FlatList } from "react-native";
import { useSpotifyAuth } from "./utils";
import { Themes } from "./assets/Themes";
import { ImageBackground } from "react-native-web";
import { C } from "caniuse-lite/data/agents";
import { warmUpAsync } from "expo-web-browser";


export default function App() {
  // Pass in true to useSpotifyAuth to use the album ID (in env.js) instead of top tracks
  const { token, tracks, getSpotifyAuth } = useSpotifyAuth(true);

 
  

  let contentDisplayed = null;

  // CODE FOUND ONLINE -- HELPER FUNCTION IS NOT MY OWN **** 
  //THIS IS USED TO CONVERT SONG LENGTH
  function millisToMinutesAndSeconds(millis) {
      var minutes = Math.floor(millis / 60000);
      var seconds = ((millis % 60000) / 1000).toFixed(0);
      return minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
    }
    
  const renderItem = (item) => {
    return (


      
      <View style={styles.row}>
        

        
          <View style={styles.track_number}>
            <Text style={styles.track_style}> {item.track_number}</Text>
          </View>
   
          <View style={styles.col1}>
        
            <Image
            style={styles.album_cover}
            
            source={{uri: item.album.images[0].url }}
            />
          </View>



          <View style={styles.col3}>
            <Text style={styles.main_text} numberOfLines={1} ellipsizeMode='tail'> {item.name} </Text>
            <Text style={styles.sub_text}>{item.artists[0].name}</Text>
          </View>
          <View style={styles.col4}>
            <Text style={styles.album_name} numberOfLines={1} ellipsizeMode='tail'>{item.album.name}</Text>
          
          </View>
          <View style={styles.col5}>
            <Text style={styles.time} numberOfLines={1} ellipsizeMode='tail' >{millisToMinutesAndSeconds(item.duration_ms)}</Text>
          </View>

        </View>

      

    )
  }

  const SpotifyAuthButton = () => {
    return(
      <Pressable  onPress={() => {
        getSpotifyAuth()
      }}
      style={({ pressed }) => [
        {
          backgroundColor: pressed
            ? 'rgb(210, 230, 255)'
            : Themes.colors.spotify
        },
        
        styles.button
      ]}>
        <Image 
        source={require('./designs/spotify_logo.png')}
        style={styles.auth_button}>
        </Image>
        <Text style={styles.text}> Connect with Spotify! </Text>

      {({ pressed }) => (
        <Text style={styles.text}>
          {pressed ? "Connecting!" : 'Connect with Spotify!'}
        </Text>

  
      )}



    </Pressable>
    )
  }


  const TrackList = () => {
    return (
      <SafeAreaView style={styles.container}> 
        <View style={styles.welcome_screen_text}>
          <Image  
          source={require('./designs/spotify_logo.png')}
          style={styles.top_tracks_logo}>

          </Image>
          <Text style={styles.top_tracks_text}>My Top Tracks</Text>
      </View>

      <FlatList
        data = {tracks}
        renderItem ={({item}) => renderItem(item)}
        keyExtractor={(item) => item.id}
    />
    </SafeAreaView>
    )

  };
  
  

      
     



 

    
    if (token) {

      console.log(tracks)
      contentDisplayed = <TrackList/>
      
    } else {
      contentDisplayed = 
      <SpotifyAuthButton/>

    }


  
  
  return (
    <SafeAreaView style={styles.container}>
     

      {contentDisplayed}


    </SafeAreaView>

  



   
  );



}

const styles = StyleSheet.create({
  container: {
    backgroundColor: Themes.colors.background,
    justifyContent: "center",
    alignItems: "center",
    flex: 1,
  },
  text: {
    fontSize: Themes.Text,
    color: Themes.colors.white,
    position: 'absolute',left:'25%', bottom:'30%',
    


  },
  main_text: {
    fontSize: 12,
    color: Themes.colors.white,
    
    flexWrap:'wrap',
  },
  sub_text: {
    fontSize: 8,
    color: Themes.colors.gray,
    position: 'absolute', bottom:'10%',
  },
  auth_button: {
    width: '18%',
    height: '100%',
    resizeMode: 'contain',
    position: 'absolute',left:'5%',
  },

  main_screen: {
    backgroundColor: 'white',
  },
  button: {
    borderRadius: 99999,
    
    width: '50%%',
    height:'5%',
  },


  row: {
    flexDirection: 'row',
    width: '100%',
    backgroundColor:Themes.colors.background,
    height: 50,
    
    
  },

 
  album_cover: {
    width: '100%',
    height: '100%',
    resizeMode:'contain',
    position:'absolute',left:'-30%',
    flexDirection: 'row',
  },
  
  track_number: {
    width: '15%',
    height: '80%',
    alignItems:'center',
    flexDirection: 'row',
    
    
  },
  col1: {
    width: '10%',
    height: '80%',
    flexDirection: 'row',
    resizeMode: 'contain',
    
    

    
  },
  col3: {
    width: '35%',
    height: '80%',
    flexDirection: 'row',
    resizeMode: 'contain',
    // backgroundColor:'yellow',
    


  },
  col4: {
    width: '20%',
    height: '80%',
    flexDirection: 'row',
    // backgroundColor:'yellow',
    

  },
  col5: {
    width: '20%',
    height: '80%',
    flexDirection: 'row',
    
    
  
  },



  track_style: {
    fontSize: 12,
    textAlign: 'center',
    position:'absolute',left:'30%', bottom:'30%',
    color: Themes.colors.gray,
    
    
  },




  welcome_screen_text: {
    flexDirection: 'row',
    height: '10%',
    
  },
  top_tracks_logo: {
    width: '20%',
    height: '30%',
    resizeMode: 'contain',
    position: 'absolute',bottom:'25%', left:'-25%',
    
  },
  top_tracks_text: {
    fontSize: 16,
    color: Themes.colors.white,
    position: 'absolute',left:'-11%',bottom:'30%',
    
    
  },
  time: {
    fontSize: 12,
    color: Themes.colors.white,
    
    position: 'absolute', left:'40%',
    flexWrap:'wrap',
  },
  album_name: {
    fontSize: 12,
    color: Themes.colors.white,
    flexWrap:'wrap',
    // position: 'absolute', left:'30%',
    
  }
});
